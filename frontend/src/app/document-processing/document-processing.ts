import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { dummyDocumentExtractionResponse  } from './document-response.mock'; // adjust path if needed
import { DocumentService } from './document.service';
import { MatIconModule } from '@angular/material/icon';
import * as ExcelJS from 'exceljs';
import * as FileSaver from 'file-saver';
import { Subscription } from 'rxjs';
import { v4 as uuidv4 } from 'uuid';


@Component({
  selector: 'app-document-processing',
  standalone: true,
  imports: [CommonModule, FormsModule,MatIconModule, ],
  templateUrl: './document-processing.html',
  styleUrls: ['./document-processing.css'],
  providers: [DocumentService]
})
export class DocumentProcessing {
  // File inputs
  docFile: File | null = null;
  fieldsFile: File | null = null;
  selectedFileName = '';
  selectedFieldsFileName = '';
  sessionId: string = ''; 
  clientId: String = '';
  isLoading = false;
  errorMessage: string | null = null;
  uploadErrorMessage: string | null = null;
  isCancelling = false;  // new flag
  toastMessage: string | null = null;
  // Input fields
  prompt = '';
  chatInput= '';
  initialPrompt: string = '';

  // States
  showDescription = false;
  viewMode: 'value' | 'document_field' | 'both' = 'value';
  // Data structures
  outputTable: string[][] = [];
  processedFields: any[] = [];
  processedFieldPairs: any[][] = [];
  chatMessages: { from: 'user' | 'bot'; text: string }[] = [];
  processSub: Subscription | null = null;
  showDownloadPopup = false;
  initialPromptSent = false;
  downloadPopupMessage = '';
  editingValueField: string | null = null;
  editingDocField: string | null = null;
  isBulkEditing = false; // controls edit mode
  backupFields: any[] = []; // stores original values for reset


  startBulkEdit() {
    this.isBulkEditing = true;
    // Deep clone for reset
    this.backupFields = JSON.parse(JSON.stringify(this.processedFields));
  }

  saveBulkEdit() {
    this.isBulkEditing = false;
    this.backupFields = [];
  }

  resetBulkEdit() {
    this.processedFields = JSON.parse(JSON.stringify(this.backupFields));
    this.isBulkEditing = false;
    this.backupFields = [];
  }



  closeDownloadPopup() {
    this.showDownloadPopup = false;
  }


  // Toggle description panel
  toggleDescription() {
    this.showDescription = !this.showDescription;
  }

  // File selection
  onFileSelected(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0] || null;
    this.docFile = file;
    this.selectedFileName = file ? file.name : '';
  }

  onFieldsSelected(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0] || null;
    this.fieldsFile = file;
    this.selectedFieldsFileName = file ? file.name : '';
  }

  

  constructor(private documentService: DocumentService) {
  // Initial AI greeting message
  this.chatMessages.push({
    from: 'bot',
    text: '💡 Ask initial prompt...'
  });
}

  processDocument() {
    this.uploadErrorMessage = null;

    if (!this.docFile || !this.fieldsFile) {
      this.uploadErrorMessage = 'Please upload both the Broker Document file and Fields Configuration file.';
      return;
    }

    this.isLoading = true;
    this.errorMessage = null;

    // Clear UI state
    this.processedFields = [];
    this.processedFieldPairs = [];
    this.outputTable = [];
    this.chatMessages = [];
    this.chatInput = '';

    // Generate session ID before request
    this.sessionId = uuidv4();

    const formData = new FormData();
    formData.append('doc', this.docFile);
    formData.append('custom_fields', this.fieldsFile);
    formData.append('client_session_id', this.sessionId); 
    
    if (this.initialPrompt) {
      formData.append('user_prompt', this.initialPrompt);
      console.log("initial prompt",this.initialPrompt);
      this.chatMessages.push({ from: 'user', text: this.initialPrompt });
    }


  
    this.processSub = this.documentService.processDocument(formData).subscribe(
      (result) => {
        this.isLoading = false;
        this.processSub = null;

        if (result.status === 'fallback') {
    this.errorMessage = 'Document processing failed. Showing fallback data.';
    setTimeout(() => (this.errorMessage = null), 6000);

    // 💡 Use fallback data from dummy
    const fallback = dummyDocumentExtractionResponse.response.rows.find((r: any) => r.index === 0);
    this.processedFields = (fallback?.fields || []).map((field: any) => ({
    ...field,
    document_field: field.document_field || field.document_label || ''
  }));

    this.processedFieldPairs = this.chunkFields(this.processedFields, 2);
    this.outputTable = this.generateDummyTable(11, 11); // optional if needed
    return;
  }


      const response = result.response;

      if (response?.session_id) {
  this.sessionId = response.session_id;
    }
      const index0 = response?.response?.rows?.find((r: any) => r.index === 0) ||
                     response?.rows?.find((r: any) => r.index === 0);

      this.processedFields = (index0?.fields || []).map((field: any) => ({
  ...field,
  document_field: field.document_field || field.document_label || ''
}));

      this.processedFieldPairs = this.chunkFields(this.processedFields, 2);
      this.outputTable = this.generateDummyTable(11, 11);
    },
    (err) => {
      this.isLoading = false;
      this.processSub = null;
      const detail = err?.error?.detail || err?.message || 'Unknown error occurred.';
      this.errorMessage = `${detail}`;
      console.error('Document API Error:', err);
    }
  );
}
  


get currentTime(): string {
  const now = new Date();
  return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}



  // Utility: Group items in chunks of N
  chunkFields(arr: any[], size: number): any[][] {
    const result: any[][] = [];
    for (let i = 0; i < arr.length; i += size) {
      result.push(arr.slice(i, i + size));
    }
    return result;
  }

  generateDummyTable(rows: number, cols: number): string[][] {
    return Array.from({ length: rows }, (_, i) =>
      Array.from({ length: cols }, (_, j) => `R${i + 1}C${j + 1}`)
    );
  }

  // Handle editable cells
  onCellEdit(event: Event, row: number, col: number) {
    const newValue = (event.target as HTMLElement).innerText.trim();
    this.outputTable[row][col] = newValue;
  }

  // Save logic
  saveMessage = '';
  sendPrompt() {
    const userMessage = this.prompt.trim();
    if (!userMessage) return;

    // Add user message to chat
    this.chatMessages.push({ from: 'user', text: userMessage });

    if (!this.outputTable.length && !this.initialPrompt) {
      // Initial prompt before processing
      this.initialPrompt = userMessage;

      // Replace "Ask initial prompt..." bot message with confirmation
      this.chatMessages.push({
        from: 'bot',
        text: '📄 Got it! Now click "Process" to extract from document.'
      });
    } else {
      // Treat as chat continuation
      this.chatInput = userMessage;
      this.sendMessage();
    }

    // Clear the prompt textbox
    this.prompt = '';
  }


saveUpdatedFields() {
  const filteredFields = this.processedFields.map(field => {
    return {
      custom_field: field.custom_field,
      document_field: field.document_field,
      value: field.value
    };
  });

  const data = {
    fields: filteredFields
  };

  const jsonData = JSON.stringify(data, null, 2);
  const blob = new Blob([jsonData], { type: 'application/json' });
  const url = URL.createObjectURL(blob);

  const a = document.createElement('a');
  a.href = url;
  a.download = 'updated_fields.json';
  a.click();

  URL.revokeObjectURL(url);

  // Show popup
  this.downloadPopupMessage = 'JSON downloaded successfully!';
  this.showDownloadPopup = true;
}


  saveUpdatedFields1() {
  const data = {
    fields: this.processedFields
  };

  const jsonData = JSON.stringify(data, null, 2);
  const blob = new Blob([jsonData], { type: 'application/json' });
  const url = URL.createObjectURL(blob);

  const a = document.createElement('a');
  a.href = url;
  a.download = 'updated_fields.json';
  a.click();

  URL.revokeObjectURL(url);

  // Show popup
  this.downloadPopupMessage = 'JSON downloaded successfully!';
  this.showDownloadPopup = true;
}


 sendMessage() {
  if (!this.chatInput.trim() || !this.sessionId) return;

  const currentPrompt = this.chatInput;
  this.chatInput = ''; // Clear before API

  this.documentService.continueChat(this.sessionId, currentPrompt).subscribe({
    next: (res) => {
      const response = res?.response;

      // Case 1: Simple bot message
      if (response?.response?.rows === null && response?.response?.message) {
        const aiReply = response.response.message;
        this.chatMessages.push({ from: 'bot', text: aiReply });
      }

      // Case 2: Fields updated
      if (response?.rows?.length) {
        const index0 = response.rows.find((r: any) => r.index === 0);
        if (index0?.fields) {
          this.processedFields = index0.fields;
          this.processedFieldPairs = this.chunkFields(this.processedFields, 2);
          this.chatMessages.push({ from: 'bot', text: 'Fields updated based on LLM response.' });
        }
      }
    },

    error: (err) => {
      const detail = err?.error?.detail || err?.message || 'Unknown error occurred.';
      const fallbackMsg = `Error from LLM: ${detail}`;
      this.chatMessages.push({ from: 'bot', text: fallbackMsg });
      console.error('LLM Chat Error:', err);
    }
  });
}



 cancelProcessing() {
  if (!this.sessionId) {
    console.log("no session id");
    return;
  }

  this.isCancelling = true;

  const formData = new FormData();
  formData.append('session_id', this.sessionId);

  // Cancel the ongoing HTTP request
  if (this.processSub) {
    this.processSub.unsubscribe();
    this.processSub = null;
  }

  this.documentService.cancelAnalysis(formData).subscribe({
    next: () => {
      this.isLoading = false;
      this.isCancelling = false;  // reset
      this.errorMessage = 'Document processing was cancelled.';
    },
    error: (err) => {
      this.isLoading = false;
      this.isCancelling = false;  // reset
      console.error('Cancellation failed:', err);
      this.errorMessage = 'Failed to cancel. Try again.';
    }
  });
}


  resetAll() {
  // Reset files
  this.docFile = null;
  this.fieldsFile = null;
  this.selectedFileName = '';
  this.selectedFieldsFileName = '';

  // Reset inputs
  this.prompt = '';
  this.chatInput = '';

  // Reset outputs and session
  this.sessionId = '';
  this.processedFields = [];
  this.processedFieldPairs = [];
  this.outputTable = [];
  this.chatMessages = [];

  // Reset flags
  this.errorMessage = null;
  this.uploadErrorMessage = null;
  this.isLoading = false;
  this.isCancelling = false;


}


  downloadExcel() {
  const workbook = new ExcelJS.Workbook();
  const worksheet = workbook.addWorksheet('Extracted Fields');

  // Add header
  const headerRow = worksheet.addRow(['User Field', 'Document Field', 'Value']);
  headerRow.font = { bold: true };
  headerRow.alignment = { horizontal: 'center' };
  headerRow.eachCell(cell => {
    cell.border = {
      top: { style: 'thin' },
      left: { style: 'thin' },
      bottom: { style: 'thin' },
      right: { style: 'thin' },
    };
  });

  // Add data
  this.processedFields.forEach(field => {
    const userField = field.user_field || field.custom_field || field.field || '';
    const docField = field.document_field || field.document_label || '';
    const value = field.value ?? '';

    const row = worksheet.addRow([userField, docField, value]);
    row.eachCell(cell => {
      cell.border = {
        top: { style: 'thin' },
        left: { style: 'thin' },
        bottom: { style: 'thin' },
        right: { style: 'thin' },
      };
      cell.alignment = { horizontal: 'left' };
    });
  });

  worksheet.columns.forEach(col => (col.width = 25));

  // Download and show popup
  workbook.xlsx.writeBuffer().then(buffer => {
    const blob = new Blob([buffer], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    });
    FileSaver.saveAs(blob, 'updated_fields.xlsx');

    //  Show modal
    this.downloadPopupMessage = 'Excel downloaded successfully!';
  this.showDownloadPopup = true;

  });
}

  
}
