import {ComponentFixture, TestBed} from '@angular/core/testing';

import {TipTranslationComponent} from './tip-translation.component';

describe('TipTranslationComponent', () => {
  let component: TipTranslationComponent;
  let fixture: ComponentFixture<TipTranslationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TipTranslationComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(TipTranslationComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
