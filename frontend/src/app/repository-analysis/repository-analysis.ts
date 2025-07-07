import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { RepositoryService } from './repository.service';
import { HttpClientModule } from '@angular/common/http';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

@Component({
  selector: 'app-repository-analysis',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
    MatIconModule,
    HttpClientModule,
  ],
  templateUrl: './repository-analysis.html',
  styleUrls: ['./repository-analysis.css']
})
export class RepositoryAnalysis {
  isExpanded = false;
  repoUrl = '';
  parsedEntities: any[] = [];
  jsonResponse: any = null;
  errorMessage: string | null = null;
  isLoading = false;

  constructor(private repoService: RepositoryService) {}

  analyzeRepo() {
  if (!this.repoUrl.trim()) {
    alert('⚠️ Please enter a repository URL before analyzing.');
    return;
  }

  // 🔄 Reset previous states
  this.jsonResponse = null;
  this.parsedEntities = [];
  this.errorMessage = null;
  this.isLoading = true;

  this.repoService.analyzeRepository(this.repoUrl).subscribe((response) => {
    console.log('📦 Full API Response:', response);

    this.isLoading = false;  // ✅ Stop loading when response received

    if (response?.status === 'success') {
      this.jsonResponse = response.response?.response;
    } else if (response?.status === 'error') {
      this.errorMessage = response.message || 'An unknown error occurred.';
      setTimeout(() => {
        this.errorMessage = null;
      }, 6000);
    }
  });
}


  getFieldKeys(fields: any[]): string[] {
  const allKeys = fields.flatMap((field) => Object.keys(field));
  return Array.from(new Set(allKeys));
}


  downloadJSON() {
    const json = JSON.stringify(this.repoService.lastResponse, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'validation-result.json';
    a.click();

    window.URL.revokeObjectURL(url);
  }



downloadPDF() {
  const doc = new jsPDF();
  let y = 10;

  doc.setFontSize(18);
  doc.text('Validation Report', 14, y);
  y += 10;

  for (const entity of this.jsonResponse?.entities || []) {
    doc.setFontSize(14);
    doc.text(entity.name, 14, y);
    y += 6;

    if (entity.note) {
      doc.setFontSize(11);
      doc.text(entity.note, 14, y);
      y += 10;
      continue;
    }

    if (entity.fields?.length) {
  const keys = this.getFieldKeys(entity.fields);
  const rows = entity.fields.map((field: any) => keys.map(k => field[k] ?? '—'));

  autoTable(doc, {
    startY: y,
    head: [keys],
    body: rows,
    theme: 'grid',
    styles: { fontSize: 9 },
    headStyles: { fillColor: [240, 173, 78] }
  });

  y = (doc as any).lastAutoTable.finalY + 10;
}

  }

  doc.save('validation-report.pdf');
}

}
