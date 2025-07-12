import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { dummyDocumentExtractionResponse  } from './document-response.mock'; // adjust path if needed
import { DocumentService } from './document.service';
import { MatIconModule } from '@angular/material/icon';

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
  if (!this.docFile || !this.fieldsFile) {
    alert('⚠️ Please upload both the document file and fields file before processing.');
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
      this.errorMessage = '⚠️ Document processing failed. Showing fallback data.';
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
  }, (err) => {
    this.isLoading = false;
    this.errorMessage = '❌ An error occurred while processing the document.';
    console.error('Error:', err);
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
  const jsonData = JSON.stringify(this.processedFields, null, 2);
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

  this.chatMessages.push({ from: 'user', text: this.chatInput });

  this.documentService.continueChat(this.sessionId, this.chatInput).subscribe((res) => {
    const response = res?.response;

    // Case 1: If bot returned a message
    if (response?.response?.rows === null && response?.response?.message) {
  this.chatMessages.push({ from: 'bot', text: response.response.message });
}


    // Case 2: If bot returned updated field rows
    if (response?.rows?.length) {
      // You can update based on specific index (e.g., index 0) or merge all
      const index0 = response.rows.find((r: any) => r.index === 0);
      if (index0?.fields) {
        this.processedFields = index0.fields;
        this.processedFieldPairs = this.chunkFields(this.processedFields, 2);

        // Add an info message to chat
        this.chatMessages.push({
          from: 'bot',
          text: '✅ Fields updated based on the latest LLM reply.'
        });
      }
    }

    this.chatInput = '';
  });
}

   downloadExcel() {
  const header = ['User Field', 'Document Field', 'Value'];
  const rows = this.processedFields.map(f => [f.user_field, f.document_field, f.value]);

  const csvContent = [header, ...rows].map(e => e.join(',')).join('\n');
  const blob = new Blob([csvContent], { type: 'text/csv' });
  const url = URL.createObjectURL(blob);

  const a = document.createElement('a');
  a.href = url;
  a.download = 'updated_fields.csv';
  a.click();

  URL.revokeObjectURL(url);
}
  
}
