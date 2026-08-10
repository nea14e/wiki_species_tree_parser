import {ComponentFixture, TestBed} from '@angular/core/testing';

import {TipOfTheDay} from './tip-of-the-day.component';

describe('TipOfTheDay', () => {
  let component: TipOfTheDay;
  let fixture: ComponentFixture<TipOfTheDay>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TipOfTheDay],
    }).compileComponents();

    fixture = TestBed.createComponent(TipOfTheDay);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
