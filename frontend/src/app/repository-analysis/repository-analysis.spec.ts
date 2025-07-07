import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RepositoryAnalysis } from './repository-analysis';

describe('RepositoryAnalysis', () => {
  let component: RepositoryAnalysis;
  let fixture: ComponentFixture<RepositoryAnalysis>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RepositoryAnalysis]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RepositoryAnalysis);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
