// File: broker-config.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { mapMetadataKeys } from './metadata-mapper';

@Injectable({
  providedIn: 'root'
})
export class BrokerConfigService {
  private dummyBrokers = [
    { 'broker-code': 'B001', 'broker-name': 'BNP' },
    { 'broker-code': 'B002', 'broker-name': 'BNA' }
  ];

  constructor(private http: HttpClient) {}

  getBrokers(): Observable<any> {
    // Simulate API call with fallback
    return this.http.get<any>('your-api-endpoint/brokers').pipe(
      catchError(() => of({ broker: this.dummyBrokers }))
    );
  }
  getTemplateCount(brokerCode: string): Observable<any> {
  //return this.http.get(`/api/brokers/${brokerCode}/template-count`);
  return of({count:4});
}

getTemplateData(payload: any): Observable<any> {
  //return this.http.post(`/api/brokers/template-data`, payload);
  const rawResponse={
      version_no: '2',
      response: {
        rows: [
          {
            index: 0,
            fields: [
              {
                custom_field: 'unique_identifier',
                document_label: 'Branch Name',
                value: 'ABC',
                metadata: {
                  'start-index-nbr': 0,
                  'end-index-nbr': 10,
                  'row_adder-cnt': 2,
                  'Col_Adder_CNT': 1,
                  'PARAM_Rref_Delim_txt': '-',
                  'Param_value_pos_cd': 'R',
                  'Unit_price_pct_ind': true,
                  'Param_nm_occur_ind': false,
                  'Date_format_cd': 'MM-DD-YYYY',
                  'Decimal_seperator_cd': '.',
                  'Param_def_value_txt': 'N/A',
                  'Derivation_col': 'D1',
                  'Operations_seq': 'Op1',
                  'Param_val_fn_txt': 'fn()'
                }
              },
              {
                custom_field: 'branchNM',
                document_label: 'Branch',
                value: 'QWR',
                metadata: {
                  'start-index-nbr': 0,
                  'end-index-nbr': 10,
                  'row_adder-cnt': 2,
                  'Col_Adder_CNT': 1,
                  'PARAM_Rref_Delim_txt': '-',
                  'Param_value_pos_cd': 'R',
                  'Unit_price_pct_ind': true,
                  'Param_nm_occur_ind': false,
                  'Date_format_cd': 'MM-DD-YYYY',
                  'Decimal_seperator_cd': '.',
                  'Param_def_value_txt': 'N/A',
                  'Derivation_col': 'D1',
                  'Operations_seq': 'Op1',
                  'Param_val_fn_txt': 'fn()'
                }
              }
            ]
          }
        ]
      }
    };

    const mappedResponse = {
    ...rawResponse,
    response: {
      rows: rawResponse.response.rows.map(row => ({
        ...row,
        fields: row.fields.map(field => ({
          ...field,
          metadata: mapMetadataKeys(field.metadata)
        }))
      }))
    }
  };

  return of(mappedResponse);


}

  submitFinalConfiguration(payload: any): Observable<any> {
  return this.http.post('/api/broker/submit-final', payload);
}


  submitBrokerConfiguration(formData: FormData): Observable<any> {
    console.log('Mock sending formData:', formData);
    const rawResponse={
      session_id: 'mockSession123',
      response: {
        rows: [
          {
            index: 0,
            fields: [
              {
                custom_field: 'branchNM',
                document_label: 'Branch Name',
                value: 'ABC',
                metadata: {
                  'start-index-nbr': 0,
                  'end-index-nbr': 10,
                  'row_adder-cnt': 2,
                  'Col_Adder_CNT': 1,
                  'PARAM_Rref_Delim_txt': '-',
                  'Param_value_pos_cd': 'R',
                  'Unit_price_pct_ind': true,
                  'Param_nm_occur_ind': false,
                  'Date_format_cd': 'MM-DD-YYYY',
                  'Decimal_seperator_cd': '.',
                  'Param_def_value_txt': 'N/A',
                  'Derivation_col': 'D1',
                  'Operations_seq': 'Op1',
                  'Param_val_fn_txt': 'fn()'
                }
              },
              {
                custom_field: 'branchNM',
                document_label: 'Branch',
                value: 'QWR',
                metadata: {
                  'start-index-nbr': 0,
                  'end-index-nbr': 10,
                  'row_adder-cnt': 2,
                  'Col_Adder_CNT': 1,
                  'PARAM_Rref_Delim_txt': '-',
                  'Param_value_pos_cd': 'R',
                  'Unit_price_pct_ind': true,
                  'Param_nm_occur_ind': false,
                  'Date_format_cd': 'MM-DD-YYYY',
                  'Decimal_seperator_cd': '.',
                  'Param_def_value_txt': 'N/A',
                  'Derivation_col': 'D1',
                  'Operations_seq': 'Op1',
                  'Param_val_fn_txt': 'fn()'
                }
              }
            ]
          }
        ]
      }
    };

    const mappedResponse = {
    ...rawResponse,
    response: {
      rows: rawResponse.response.rows.map(row => ({
        ...row,
        fields: row.fields.map(field => ({
          ...field,
          metadata: mapMetadataKeys(field.metadata)
        }))
      }))
    }
  };

  return of(mappedResponse);
  }


setUniqueIdentifier(payload: any): Observable<any> {
  console.log('Mock: Setting unique identifier with payload:', payload);
  const rawResponse={
    response: {
      rows: [
        {
          index: 0,
          fields: [
            // Return updated field list (just returning previous dummy for now)
            {
              custom_field: 'branchNM',
              document_label: 'Branch Name',
              value: 'ABC',
              metadata: {
                'start-index-nbr': 0,
                'end-index-nbr': 10,
                'row_adder-cnt': 2,
                'Col_Adder_CNT': 1,
                'PARAM_Rref_Delim_txt': '-',
                'Param_value_pos_cd': 'R',
                'Unit_price_pct_ind': true,
                'Param_nm_occur_ind': false,
                'Date_format_cd': 'MM-DD-YYYY',
                'Decimal_seperator_cd': '.',
                'Param_def_value_txt': 'N/A',
                'Derivation_col': 'D1',
                'Operations_seq': 'Op1',
                'Param_val_fn_txt': 'fn()'
              }
            },
             {
                custom_field: 'branchNM',
                document_label: 'Branch',
                value: 'QWR',
                metadata: {
                  'start-index-nbr': 0,
                  'end-index-nbr': 10,
                  'row_adder-cnt': 2,
                  'Col_Adder_CNT': 1,
                  'PARAM_Rref_Delim_txt': '-',
                  'Param_value_pos_cd': 'R',
                  'Unit_price_pct_ind': true,
                  'Param_nm_occur_ind': false,
                  'Date_format_cd': 'MM-DD-YYYY',
                  'Decimal_seperator_cd': '.',
                  'Param_def_value_txt': 'N/A',
                  'Derivation_col': 'D1',
                  'Operations_seq': 'Op1',
                  'Param_val_fn_txt': 'fn()'
                }
              },
            {
              custom_field: payload.field_name,
              document_label: payload.field_name,
              value: 'CustomVal123',
              metadata: {
                'start-index-nbr': 0,
                  'end-index-nbr': 10,
                  'row_adder-cnt': 2,
                  'Col_Adder_CNT': 1,
                  'PARAM_Rref_Delim_txt': '-',
                  'Param_value_pos_cd': 'R',
                  'Unit_price_pct_ind': true,
                  'Param_nm_occur_ind': false,
                  'Date_format_cd': 'MM-DD-YYYY',
                  'Decimal_seperator_cd': '.',
                  'Param_def_value_txt': 'N/A',
                  'Derivation_col': 'D1',
                  'Operations_seq': 'Op1',
                  'Param_val_fn_txt': 'fn()'
              }
            }
          ]
        }
      ]
    }
  };
  const mappedResponse = {
    ...rawResponse,
    response: {
      rows: rawResponse.response.rows.map(row => ({
        ...row,
        fields: row.fields.map(field => ({
          ...field,
          metadata: mapMetadataKeys(field.metadata)
        }))
      }))
    }
  };

  return of(mappedResponse);
}

validateUniqueIdentifier(payload: any): Observable<any> {
  console.log('Mock: Validating identifier for:', payload);
  const isValid = payload.field_name?.toLowerCase().includes('branch');
  return of({ valid: isValid });
}

initialAdd(payload: any): Observable<any> {
  console.log('Mock: Initial prompt submitted with payload:', payload);
  const rawResponse={
    response: {
      rows: [
        {
          index: 0,
          fields: [
            // Return updated field list (just returning previous dummy for now)
            {
              custom_field: 'branchNM',
              document_label: 'Branch Name',
              value: 'ABC',
              metadata: {
                'start-index-nbr': 0,
                'end-index-nbr': 10,
                'row_adder-cnt': 2,
                'Col_Adder_CNT': 1,
                'PARAM_Rref_Delim_txt': '-',
                'Param_value_pos_cd': 'R',
                'Unit_price_pct_ind': true,
                'Param_nm_occur_ind': false,
                'Date_format_cd': 'MM-DD-YYYY',
                'Decimal_seperator_cd': '.',
                'Param_def_value_txt': 'N/A',
                'Derivation_col': 'D1',
                'Operations_seq': 'Op1',
                'Param_val_fn_txt': 'fn()'
              }
            },
             {
                custom_field: 'branchNM',
                document_label: 'Branch',
                value: 'QWR',
                metadata: {
                  'start-index-nbr': 0,
                  'end-index-nbr': 10,
                  'row_adder-cnt': 2,
                  'Col_Adder_CNT': 1,
                  'PARAM_Rref_Delim_txt': '-',
                  'Param_value_pos_cd': 'R',
                  'Unit_price_pct_ind': true,
                  'Param_nm_occur_ind': false,
                  'Date_format_cd': 'MM-DD-YYYY',
                  'Decimal_seperator_cd': '.',
                  'Param_def_value_txt': 'N/A',
                  'Derivation_col': 'D1',
                  'Operations_seq': 'Op1',
                  'Param_val_fn_txt': 'fn()'
                }
              },
            {
              custom_field: payload.field_name,
              document_label: payload.field_name,
              value: 'CustomVal123',
              metadata: {
                'start-index-nbr': 0,
                  'end-index-nbr': 10,
                  'row_adder-cnt': 2,
                  'Col_Adder_CNT': 1,
                  'PARAM_Rref_Delim_txt': '-',
                  'Param_value_pos_cd': 'R',
                  'Unit_price_pct_ind': true,
                  'Param_nm_occur_ind': false,
                  'Date_format_cd': 'MM-DD-YYYY',
                  'Decimal_seperator_cd': '.',
                  'Param_def_value_txt': 'N/A',
                  'Derivation_col': 'D1',
                  'Operations_seq': 'Op1',
                  'Param_val_fn_txt': 'fn()'
              }
            }
          ]
        }
      ]
    }
  };
  const mappedResponse = {
    ...rawResponse,
    response: {
      rows: rawResponse.response.rows.map(row => ({
        ...row,
        fields: row.fields.map(field => ({
          ...field,
          metadata: mapMetadataKeys(field.metadata)
        }))
      }))
    }
  };

  return of(mappedResponse);
}
continueChat(payload: any): Observable<any> {
  console.log('Mock: Follow-up prompt received with payload:', payload);
  const rawResponse={
    response: {
      rows: [
        {
          index: 0,
          fields: [
            // Return updated field list (just returning previous dummy for now)
            {
              custom_field: 'branchNM',
              document_label: 'Branch Name',
              value: 'ABC',
              metadata: {
                'start-index-nbr': 0,
                'end-index-nbr': 10,
                'row_adder-cnt': 2,
                'Col_Adder_CNT': 1,
                'PARAM_Rref_Delim_txt': '-',
                'Param_value_pos_cd': 'R',
                'Unit_price_pct_ind': true,
                'Param_nm_occur_ind': false,
                'Date_format_cd': 'MM-DD-YYYY',
                'Decimal_seperator_cd': '.',
                'Param_def_value_txt': 'N/A',
                'Derivation_col': 'D1',
                'Operations_seq': 'Op1',
                'Param_val_fn_txt': 'fn()'
              }
            },
             {
                custom_field: 'branchNM',
                document_label: 'Branch',
                value: 'QWR',
                metadata: {
                  'start-index-nbr': 0,
                  'end-index-nbr': 10,
                  'row_adder-cnt': 2,
                  'Col_Adder_CNT': 1,
                  'PARAM_Rref_Delim_txt': '-',
                  'Param_value_pos_cd': 'R',
                  'Unit_price_pct_ind': true,
                  'Param_nm_occur_ind': false,
                  'Date_format_cd': 'MM-DD-YYYY',
                  'Decimal_seperator_cd': '.',
                  'Param_def_value_txt': 'N/A',
                  'Derivation_col': 'D1',
                  'Operations_seq': 'Op1',
                  'Param_val_fn_txt': 'fn()'
                }
              },
            {
              custom_field: payload.field_name,
              document_label: payload.field_name,
              value: 'CustomVal123',
              metadata: {
                'start-index-nbr': 0,
                  'end-index-nbr': 10,
                  'row_adder-cnt': 2,
                  'Col_Adder_CNT': 1,
                  'PARAM_Rref_Delim_txt': '-',
                  'Param_value_pos_cd': 'R',
                  'Unit_price_pct_ind': true,
                  'Param_nm_occur_ind': false,
                  'Date_format_cd': 'MM-DD-YYYY',
                  'Decimal_seperator_cd': '.',
                  'Param_def_value_txt': 'N/A',
                  'Derivation_col': 'D1',
                  'Operations_seq': 'Op1',
                  'Param_val_fn_txt': 'fn()'
              }
            }
          ]
        }
      ]
    }
  };
  const mappedResponse = {
    ...rawResponse,
    response: {
      rows: rawResponse.response.rows.map(row => ({
        ...row,
        fields: row.fields.map(field => ({
          ...field,
          metadata: mapMetadataKeys(field.metadata)
        }))
      }))
    }
  };

  return of(mappedResponse);
}


}
