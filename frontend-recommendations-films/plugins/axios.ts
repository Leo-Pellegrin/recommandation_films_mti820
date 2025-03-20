import axios from 'axios'
import type { AxiosInstance } from 'axios'


export default defineNuxtPlugin((nuxtApp) => {
  const api: AxiosInstance = axios.create({
    baseURL: useRuntimeConfig().public.apiBase, // Prend l'URL de ton API depuis `.env`
    headers: {
      'Content-Type': 'application/json'
    }
  })

  return {
    provide: {
      api
    }
  }
})