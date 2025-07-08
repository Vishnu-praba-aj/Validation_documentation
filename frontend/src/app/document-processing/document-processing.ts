import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { dummyDocumentExtractionResponse  } from './document-response.mock'; // adjust path if needed
import { DocumentService } from './document.service';
import { MatIconModule } from '@angular/material/icon';
import * as ExcelJS from 'exceljs';
import * as FileSaver from 'file-saver';

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
  sessionId: string = ''; // Add this to your class
  isLoading = false;
  errorMessage: string | null = null;
  uploadErrorMessage: string | null = null;

  // Input fields
  prompt = '';
  chatInput = '';

  // States
  showDescription = false;
  viewMode: 'value' | 'document_field' = 'value';

  // Data structures
  outputTable: string[][] = [];
  processedFields: any[] = [];
  processedFieldPairs: any[][] = [];
  chatMessages: { from: 'user' | 'bot'; text: string }[] = [];

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

  constructor(private documentService: DocumentService) {}
  // Simulate document processing
processDocument() {

  this.uploadErrorMessage = null;

  if (!this.docFile || !this.fieldsFile) {
    this.uploadErrorMessage = 'Please upload both the Document file and Fields Configuration file.';
    return;
  }

  this.isLoading = true;
  this.errorMessage = null;

  // 🔄 Clear UI state
  this.processedFields = [];
  this.processedFieldPairs = [];
  this.outputTable = [];
  this.chatMessages = [];
  this.chatInput = '';
  this.sessionId = '';

  const formData = new FormData();
  formData.append('doc', this.docFile);
  formData.append('custom_fields', this.fieldsFile);
  if (this.prompt) {
    formData.append('user_prompt', this.prompt);
  }

  this.documentService.processDocument(formData).subscribe((result) => {
    this.isLoading = false;

    if (result.status === 'fallback') {
      this.errorMessage = 'Document processing failed. Showing fallback data.';
      setTimeout(() => (this.errorMessage = null), 6000);
    }

    const response = result.response;

    if (response?.session_id) {
      this.sessionId = response.session_id;
    }

    const index0 = response?.response?.rows?.find((r: any) => r.index === 0) ||
                   response?.rows?.find((r: any) => r.index === 0);

    this.processedFields = index0?.fields || [];
    this.processedFieldPairs = this.chunkFields(this.processedFields, 2);
    this.outputTable = this.generateDummyTable(11, 11);
  },(err) => {
  this.isLoading = false;

  // Get backend error message
  const detail = err?.error?.detail || err?.message || 'Unknown error occurred.';
  this.errorMessage = `${detail}`;
  
  console.error('Document API Error:', err);
});
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

  saveUpdatedFields() {
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
}


 sendMessage() {
  if (!this.chatInput.trim() || !this.sessionId) return;

  // Add user message
  this.chatMessages.push({ from: 'user', text: this.chatInput });

  // Clear input immediately
  const currentPrompt = this.chatInput;
  this.chatInput = '';

  // Now send to backend
  this.documentService.continueChat(this.sessionId, currentPrompt).subscribe((res) => {
    const response = res?.response;

    // Case 1: Bot message
    if (response?.response?.rows === null && response?.response?.message) {
      this.chatMessages.push({ from: 'bot', text: response.response.message });
    }

    // Case 2: Bot updates fields
    if (response?.rows?.length) {
      const index0 = response.rows.find((r: any) => r.index === 0);
      if (index0?.fields) {
        this.processedFields = index0.fields;
        this.processedFieldPairs = this.chunkFields(this.processedFields, 2);

        this.chatMessages.push({
          from: 'bot',
          text: ' Fields updated based on the latest LLM reply.'
        });
      }
    }
  });
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

  // Add rows safely
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

  // Column sizing
  worksheet.columns.forEach(col => {
    col.width = 25;
  });

  // Download
  workbook.xlsx.writeBuffer().then(buffer => {
    const blob = new Blob([buffer], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    });
    FileSaver.saveAs(blob, 'updated_fields.xlsx');
  });
}

  
}
