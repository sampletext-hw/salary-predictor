import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {PredictRequest} from "../interfaces/predict-request";
import {PredictResponse} from "../interfaces/predict-response";
import {environment} from "../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class PredictionService {

  constructor(
    private httpClient: HttpClient
  ) { }

  public predict(request: PredictRequest): Observable<PredictResponse>{
    return this.httpClient.post<PredictResponse>(`${environment.baseUrl}/predict`, request)
  }
}
