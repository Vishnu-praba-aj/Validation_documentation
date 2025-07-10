import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { dummyDocumentExtractionResponse } from './document-response.mock';
import { of } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DocumentService {
  private baseUrl = 'http://localhost:8000/document';

  constructor(private http: HttpClient) {}

  cancelAnalysis(formData: FormData): Observable<any> {
    return this.http
      .post('http://localhost:8000/document/cancel_analysis/', formData)
      .pipe(
        catchError((err: HttpErrorResponse) => {
          console.error('Cancellation failed:', err);
          return throwError(() => err);
        })
      );
  }

  processDocument(formData: FormData): Observable<any> {
    return this.http.post(`${this.baseUrl}/extract_fields/`, formData).pipe(
      map((response) => ({ status: 'success', response })),
      catchError((err: HttpErrorResponse) => {
        console.error('Document processing failed:', err);
        return of({
          status: 'fallback',
          response: dummyDocumentExtractionResponse,
        });
      })
    );
  }

  continueChat(sessionId: string, prompt: string): Observable<any> {
    const formData = new FormData();
    formData.append('session_id', sessionId);
    formData.append('prompt', prompt);

    return this.http.post(`${this.baseUrl}/continue_chat/`, formData).pipe(
      catchError((err: HttpErrorResponse) => {
        console.error('Chat continuation failed:', err);
        return throwError(() => err);
      })
    );
  }
}
