export const dummyDocumentExtractionResponse = {
  session_id: 'a1b2c3d4-5678-90ef-ghij-klmnopqrstuv',
  type: 'document_extraction',
  response: {
    rows: [
      {
        index: 0,
        fields: [
          {
            custom_field: 'ISIN',
            document_label: 'ISIN Code',
            value: 'US1234567890'
          },
          {
            custom_field: 'Trade Date',
            document_label: 'Trade Date',
            value: '2024-06-01'
          },
          { custom_field: 'Nominal Amount',
            document_field: 'Amount',
            value: '350,000.00' 
           },

            { custom_field: 'Settlement Date', 
             document_field: 'Settlement Date', 
             value: 'May 24, 2020' 
            },
             {
            custom_field: 'ISIN',
            document_label: 'ISIN Code',
            value: 'US1234567890'
          },
          {
            custom_field: 'Trade Date',
            document_label: 'Trade Date',
            value: '2024-06-01'
          },
          { custom_field: 'Nominal Amount',
            document_field: 'Amount',
            value: '350,000.00' 
           },

            { custom_field: 'Settlement Date', 
             document_field: 'Settlement Date', 
             value: 'May 24, 2020' 
            },
            {
            custom_field: 'Trade Date',
            document_label: 'Trade Date',
            value: '2024-06-01'
          },
          { custom_field: 'Nominal Amount',
            document_field: 'Amount',
            value: '350,000.00' 
           },
        ]
      },
      {
        index: 1,
        fields: [
          {
            custom_field: 'ISIN',
            document_label: 'ISIN Code',
            value: 'US9876543210'
          },
          {
            custom_field: 'Trade Date',
            document_label: 'Trade Date',
            value: '2024-06-02'
          }
        ]
      }
    ]
  }
};
