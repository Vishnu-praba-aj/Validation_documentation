// File: new-broker-config.component.ts
import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { BrokerConfigService } from './broker-config.service';
import { MatSnackBar } from '@angular/material/snack-bar';


interface Broker {
  'broker-code': string;
  'broker-name': string;
}

interface FieldMetadata {
  [key: string]: any;
}

interface Field {
  custom_field: string;
  document_label: string;
  value: string;
  metadata: FieldMetadata;
}

@Component({
  selector: 'app-new-broker-config',
  templateUrl: './new-broker-config.html',
  styleUrls: ['./new-broker-config.css'],
  encapsulation: ViewEncapsulation.None,
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatMenuModule
  ]
})
export class NewBrokerConfig implements OnInit {
  brokers: Broker[] = [];
  selectedBrokerCode: string = '';
  documentFile: File | null = null;
  customFieldFile: File | null = null;
  prompt: string = '';
  selectedFileName: string = '';
  selectedFieldsFileName: string = '';
  responseData: Field[] = [];
  isEditing: boolean = false;
  sessionId: string = '';
  expandedCardIndex: number = -1;
  backupFields: Field[] = [];
  selectedIdentifierField: string = '';
  newIdentifierFieldName: string = '';
  optionalPhrase: string = '';
  identifierSet: boolean = false;
  promptHistory: { from: 'user' | 'bot', text: string }[] = [];
  initialPrompt: string = '';
  uniqueIdentifierField: any = null;


  constructor(
    private fb: FormBuilder,
    private brokerService: BrokerConfigService,
    private snackBar: MatSnackBar
  ) {}


  ngOnInit(): void {
    this.fetchBrokers();
  }

  fetchBrokers() {
    this.brokerService.getBrokers().subscribe(data => {
      this.brokers = data.broker;
    });
  }

  onBrokerChange(code: string) {
    this.selectedBrokerCode = code;
  }

  onFileSelected(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
    this.documentFile = file || null;
    this.selectedFileName = file ? file.name : '';
  }

  onFieldsSelected(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
    this.customFieldFile = file || null;
    this.selectedFieldsFileName = file ? file.name : '';
  }
  canAdd(): boolean {
  return !!(this.selectedBrokerCode && this.documentFile && this.customFieldFile);
}

canReset(): boolean {
  return (
    this.selectedBrokerCode !== '' ||
    this.documentFile !== null ||
    this.customFieldFile !== null ||
    this.prompt.trim().length > 0 ||
    this.responseData.length > 0
  );
}
keyvalueCompare = (a: any, b: any): number => {
  return a.key.localeCompare(b.key);
};

trackByKey(index: number, item: any): string {
  return item.key;
}

getMetadataValue(field: any, key: any): any {
  return field.metadata[key as string];
}

setMetadataValue(field: any, key: any, value: any): void {
  field.metadata[key as string] = value;
}

  onAdd() {
  const formData = new FormData();
  formData.append('broker_code', this.selectedBrokerCode);
  if (this.documentFile) formData.append('document_file', this.documentFile);
  if (this.customFieldFile) formData.append('custom_field_file', this.customFieldFile);
  if (this.prompt) formData.append('prompt', this.initialPrompt);
  console.log(this.initialPrompt);

  this.brokerService.submitBrokerConfiguration(formData).subscribe(res => {
    this.sessionId = res.session_id;
    this.responseData = res.response.rows[0].fields;
    this.expandedCardIndex = -1; // Reset expanded card
  });
}
onPromptSend() {
  if (!this.prompt.trim()) return;

  if (!this.sessionId) {
    this.initialPrompt = this.initialPrompt+' '+this.prompt;  
    this.promptHistory.push({ from: 'user', text: this.prompt });
    this.promptHistory.push({ from: 'bot', text: 'Now click Add to proceed.' });
  } else {
    this.callFollowUpAPI(this.sessionId, this.prompt);
    
  }

  this.prompt = '';
  setTimeout(() => {
  const chatBox = document.querySelector('.chat-prompt-box');
  if (chatBox) chatBox.scrollTop = chatBox.scrollHeight;
}, 30);

}

callInitialAddAPI(prompt: string) {

  const payload = {
    prompt: prompt,
    documentFile: this.documentFile,
    fieldsFile: this.customFieldFile,
    brokerCode: this.selectedBrokerCode
  };

  this.brokerService.initialAdd(payload).subscribe((response: any) => {
    this.sessionId = response.session_id;
    this.responseData = response.fields; 
  });
}

callFollowUpAPI(sessionId: string, prompt: string) {
  const payload = {
    session_id: sessionId,
    prompt: prompt
  };

  this.brokerService.continueChat(payload).subscribe((response: any) => {
    this.responseData = response.updatedFields;
    this.promptHistory.push({ from: 'user', text: this.prompt });
    this.promptHistory.push({ from: 'bot', text: "The fields got updated, please look the data." });
  });
}

toggleMetadata(index: number) {
  this.expandedCardIndex = this.expandedCardIndex === index ? -1 : index;
}
getMetadataEntries(metadata: { [key: string]: any }) {
  return Object.entries(metadata);
}

onIdentifierChange(value: string) {
  this.newIdentifierFieldName = '';
  this.optionalPhrase = '';
}

addCustomUniqueIdentifier() {
  if (!this.newIdentifierFieldName.trim()) {
    alert('Please enter a field name.');
    return;
  }
  const payload = {
    session_id: this.sessionId,
    broker_code: this.selectedBrokerCode,
    field_name: this.newIdentifierFieldName,
    phrase: this.optionalPhrase || ''
  };

  this.brokerService.setUniqueIdentifier(payload).subscribe((res: any) => {
    this.responseData = res.response.rows[0].fields;
    this.identifierSet = true;
    this.snackBar.open('Identifier added successfully!', 'Close', {
        panelClass: ['snack-success']
      });
  });
}

validateExistingIdentifier() {
  const payload = {
    broker_code: this.selectedBrokerCode,
    field_name: this.selectedIdentifierField
  };

  this.brokerService.validateUniqueIdentifier(payload).subscribe((res: any) => {
    if (res.valid) {
      this.identifierSet = true;

      const matchedField = this.responseData.find(
        f => f.document_label === this.selectedIdentifierField
      );

      if (matchedField) {
        this.uniqueIdentifierField = { ...matchedField }; 
      }

      this.snackBar.open('Identifier added successfully!', 'Close', {
        panelClass: ['snack-success']
      });
    } else {
      this.snackBar.open("Can't use this as unique identifier.", 'Close', {
        panelClass: ['snack-error']
      });
    }
  });
}


onSubmit() {
  const finalResponseData = [...this.responseData];

  if (this.uniqueIdentifierField) {
  
    const identifierFieldCopy = { ...this.uniqueIdentifierField, is_unique_identifier: true };

    finalResponseData.push(identifierFieldCopy);
  }

  const payload = {
    broker_code: this.selectedBrokerCode,
    session_id: this.sessionId,
    response: finalResponseData
  };

  console.log('Submitting payload:', payload);

  this.brokerService.submitFinalConfiguration(payload).subscribe({
    next: (res) => {
      this.snackBar.open('Configuration submitted successfully!', 'Close', {
        panelClass: ['snack-success'],
        horizontalPosition: 'center',
        verticalPosition: 'top'
      });
    },
    error: (err) => {
      console.error('Submission failed:', err);
      this.snackBar.open('Failed to submit configuration.', 'Close', {
        panelClass: ['snack-error'],
        horizontalPosition: 'center',
        verticalPosition: 'top'
      });
    }
  });
}


  toggleEdit() {
  this.backupFields = JSON.parse(JSON.stringify(this.responseData)); // deep copy
  this.isEditing = true;
}

onSave() {
  this.isEditing = false;
}

onFormReset() {
  this.selectedBrokerCode = '';
  this.documentFile = null;
  this.customFieldFile = null;
  this.prompt = '';
  this.selectedFileName = '';
  this.selectedFieldsFileName = '';
  this.responseData = [];
  this.selectedIdentifierField = '';
  this.newIdentifierFieldName = '';
  this.optionalPhrase = '';
  this.identifierSet = false;
  this.isEditing = false;
  this.expandedCardIndex = -1;
}

onEditReset() {
  this.toggleEdit();
  this.onAdd(); 
}


}
