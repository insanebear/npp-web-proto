import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { AppStateProvider } from './shared/contexts/AppStateContext'

import { BrowserRouter } from 'react-router-dom';
import App from './App.tsx'

import './index.css'
import Layout from './shared/components/NavigationBar/layout.tsx' 

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
    <AppStateProvider>
      <Layout>
        <App />
      </Layout>
    </AppStateProvider>
    </BrowserRouter>
  </StrictMode>,
)
