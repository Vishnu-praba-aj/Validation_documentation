// document.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { dummyDocumentExtractionResponse } from './document-response.mock';

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
      console.warn('Document processing failed. Using fallback.', err);  // ← ADD THIS!
      return of({
        status: 'fallback',
        response: dummyDocumentExtractionResponse
      });
    })
  );
}


  continueChat(sessionId: string, prompt: string): Observable<any> {
  const formData = new FormData();
  formData.append('session_id', sessionId);
  formData.append('prompt', prompt);

  return this.http.post(`${this.baseUrl}/continue_chat/`, formData).pipe(
    catchError(err => {
      console.warn('Chat continuation failed, using dummy fallback.', err);

      // Dummy response with message and rows
      const dummyResponse = {
        session_id: sessionId,
        type: 'document_extraction',
        response: {
          message: '⚠️ Using mock data due to API failure.',
          rows: [
            {
              index: 0,
              fields: [
                {
                  custom_field: 'charges',
                  document_label: 'Total Market Charges',
                  value: '1234.56'
                },
                {
                  custom_field: 'netAmt',
                  document_label: 'Net Amount',
                  value: '654321.00'
                },
                {
                  custom_field: 'currencyCd',
                  document_label: 'Currency',
                  value: 'INR'
                },
                {
                  custom_field: 'isinCd',
                  document_label: 'ISIN/IISIN',
                  value: 'IN1234567890'
                },
                {
                  custom_field: 'settlementDt',
                  document_label: 'Settlement Date',
                  value: '2022-05-01'
                },
                {
                  custom_field: 'tradeDt',
                  document_label: 'Trade Date',
                  value: '2022-04-28'
                },
                {
                  custom_field: 'transactionType',
                  document_label: 'Buy/Sell',
                  value: 'Buy'
                },
                {
                  custom_field: 'unitpx',
                  document_label: 'Price',
                  value: '98.76'
                }
              ]
            }
          ]
        }
      };

      return of(dummyResponse);
    })
  );
}


}
