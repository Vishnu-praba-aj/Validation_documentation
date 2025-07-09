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
  styleUrls: ['./repository-analysis.css']
})
export class RepositoryAnalysis {
  isExpanded = false;
  repoUrl = '';
  parsedEntities: any[] = [];
  jsonResponse: any = "";
  errorMessage: string | null = "";
  analyzeSub: Subscription | null = null; // Track subscription
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

  // Save subscription for cancel
  this.analyzeSub = this.repoService.analyzeRepository(this.repoUrl).subscribe((response) => {
    this.isLoading = false;

    // ✅ If actual response or fallback
    if (response?.status === 'success' || response?.status === 'fallback') {
      this.jsonResponse = response.response;

      if (response.status === 'fallback') {
        this.errorMessage = response.message || 'Fallback: Unable to analyze repo, using mock data.';
        setTimeout(() => (this.errorMessage = null), 6000);
      }

    } else {
      // Regular error
      this.errorMessage = response.message || 'An unknown error occurred.';
      setTimeout(() => (this.errorMessage = null), 6000);
    }
  });
}

  


  cancelAnalysis() {
  if (this.analyzeSub) {
    this.analyzeSub.unsubscribe(); // Cancel frontend request
  }

  this.repoService.cancelBackendProcessing(this.repoUrl); // Signal backend
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
  // Assume you generate the PDF blob here (not shown)
  // Save the file
  const blob = new Blob([/* your PDF data */], { type: 'application/pdf' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'validation_report.pdf';
  a.click();
  URL.revokeObjectURL(url);

  // Show popup
  this.downloadPopupMessage = 'PDF report downloaded successfully!';
  this.showDownloadPopup = true;
}

}
