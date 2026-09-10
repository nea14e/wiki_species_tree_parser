import {ComponentFixture, TestBed} from '@angular/core/testing';

import {FillingStatsComponent} from './filling-stats.component';

describe('FillingStatsComponent', () => {
  let component: FillingStatsComponent;
  let fixture: ComponentFixture<FillingStatsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FillingStatsComponent],
    }).compileComponents();

    fixture = TestBed.createComponent(FillingStatsComponent);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
