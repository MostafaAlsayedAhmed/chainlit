import AppWrapper from 'AppWrapper'; 
// import { apiClient } from 'api';
import React from 'react';
import ReactDOM from 'react-dom/client';
import { RecoilRoot } from 'recoil';

import { ChainlitAPI, ChainlitContext } from '@chainlit/react-client';

import './index.css';
// import './assets/styles/_custom-style.scss';
import '../../public/custom_style.css';

import { i18nSetupLocalization } from './i18n'; 
i18nSetupLocalization();

const CHAINLIT_SERVER_URL = 'http://localhost:8000';
const apiClient = new ChainlitAPI(CHAINLIT_SERVER_URL, 'webapp');


ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <ChainlitContext.Provider value={apiClient}>
      <RecoilRoot>
        <AppWrapper /> 
      </RecoilRoot>
    </ChainlitContext.Provider>
  </React.StrictMode>
);
