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
import { Subscription } from 'rxjs';

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
  styleUrls: ['./repository-analysis.css'],
})
export class RepositoryAnalysis {
  isExpanded = false;
  repoUrl = '';
  parsedEntities: any[] = [];
  jsonResponse: any = '';
  errorMessage: string | null = '';
  analyzeSub: Subscription | null = null;
  isLoading = false;
  isCancelled = false;
  showDownloadPopup = false;
  downloadPopupMessage = '';

  constructor(private repoService: RepositoryService) {}

  resetAnalysis() {
    this.repoUrl = '';
    this.jsonResponse = null;
    this.parsedEntities = [];
    this.errorMessage = null;
    this.isLoading = false;
    this.repoService.lastResponse = null;
  }

  analyzeRepo() {
    if (!this.repoUrl.trim()) {
      alert('Please enter a repository URL before analyzing.');
      return;
    }

    this.isCancelled = false;
    this.isLoading = true;
    this.jsonResponse = null;
    this.errorMessage = null;

    this.analyzeSub = this.repoService
      .analyzeRepository(this.repoUrl)
      .subscribe((response) => {
        this.isLoading = false;

        if (response?.status === 'success' || response?.status === 'fallback') {
          this.jsonResponse = response.response;

          if (response.status === 'fallback') {
            this.errorMessage =
              response.message ||
              'Fallback: Unable to analyze repo, using mock data.';
            setTimeout(() => (this.errorMessage = null), 6000);
          }
        } else {
          this.errorMessage = response.message || 'An unknown error occurred.';
          setTimeout(() => (this.errorMessage = null), 6000);
        }
      });
  }

  cancelAnalysis() {
    if (this.analyzeSub) {
      this.analyzeSub.unsubscribe();
    }

    this.repoService.cancelBackendProcessing(this.repoUrl);
    this.isLoading = false;
    this.analyzeSub = null;
  }

  getFieldKeys(fields: any[]): string[] {
    const allKeys = fields.flatMap((field) => Object.keys(field));
    return Array.from(new Set(allKeys));
  }

  closePopup() {
    this.showDownloadPopup = false;
    this.downloadPopupMessage = '';
  }

  downloadJSON() {
    const jsonData = JSON.stringify(this.jsonResponse, null, 2);
    const blob = new Blob([jsonData], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'validation_report.json';
    a.click();
    URL.revokeObjectURL(url);

    // Show popup
    this.downloadPopupMessage = 'JSON report downloaded successfully!';
    this.showDownloadPopup = true;
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
        const rows = entity.fields.map((field: any) =>
          keys.map((k) => field[k] ?? '—')
        );

        autoTable(doc, {
          startY: y,
          head: [keys],
          body: rows,
          theme: 'grid',
          styles: { fontSize: 9 },
          headStyles: { fillColor: [240, 173, 78] },
        });

        y = (doc as any).lastAutoTable.finalY + 10;
      }
    }

    doc.save('validation-report.pdf');
  }
}
