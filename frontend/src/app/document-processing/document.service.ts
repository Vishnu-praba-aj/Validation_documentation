import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class DocumentService {
  private baseUrl = 'http://localhost:8000/document';

  constructor(private http: HttpClient) {}

  processDocument(formData: FormData): Observable<any> {
    return this.http.post(`${this.baseUrl}/extract_fields/`, formData).pipe(
      map(response => ({ status: 'success', response })),
      catchError((err: HttpErrorResponse) => {
        console.error('Document processing failed:', err);
        return throwError(() => err);
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
