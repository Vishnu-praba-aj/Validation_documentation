import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RepositoryService {
  private baseUrl = 'http://localhost:8000/validation';
  lastResponse: any;

  constructor(private http: HttpClient) {}

  cancelBackendProcessing(repoUrl: string) {
  return this.http.post('http://localhost:8000/validation/cancel_analysis/', { repo_url: repoUrl })
    .subscribe({
      next: () => console.log('Backend cancel signal sent'),
      error: err => console.error('Failed to cancel backend processing:', err)
    });
}

  analyzeRepository(repoUrl: string): Observable<any> {
  const body = { repo_url: repoUrl };

  return new Observable(observer => {
    this.http.post(`${this.baseUrl}/analyze_repo/`, body).subscribe({
      next: (res) => {
        this.lastResponse = res;
        observer.next({ status: 'success', response: res });
        observer.complete();
      },
      error: (err) => {
        console.error('Validation API failed:', err);

        // Debug structure
        console.log('Full error object:', err);
        console.log('err.error:', err.error);

        const rawMessage =
          typeof err?.error === 'string'
            ? err.error
            : err?.error?.detail || 'An unexpected error occurred.';
        const message = rawMessage.replace(/^\d{3}:\s*/, '');

        // Use dummy fallback response
        const dummy = this.getDummyResponse();
        this.lastResponse = dummy;

        observer.next({
          status: 'fallback',
          message: message,
          response: dummy
        });
        observer.complete();
      }
    });
  });
}


  private getDummyResponse() {
    return {
      entities: [
        {
          name: 'FallbackUser',
          fields: [
            {
              field: 'username',
              type: 'String',
              required: true
            },
            {
              field: 'email',
              type: 'String',
              required: true,
              otherValidation: 'Must be a valid email'
            }
          ]
        },
        {
          name: 'FallbackSettings',
          fields: [
            {
              field: 'theme',
              type: 'String',
              required: false
            },
            {
              field: 'notifications',
              type: 'Boolean',
              required: true
            }
          ]
        }
      ]
    };
  }
}
