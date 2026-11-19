import {ComponentFixture, TestBed} from '@angular/core/testing';

import {EditTipTranslationComponent} from './edit-tip-translation.component';

describe('EditTipTranslationComponent', () => {
  let component: EditTipTranslationComponent;
  let fixture: ComponentFixture<EditTipTranslationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditTipTranslationComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(EditTipTranslationComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
