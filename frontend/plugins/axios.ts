import axios from 'axios'
import type { AxiosInstance } from 'axios'


export default defineNuxtPlugin((nuxtApp) => {
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase as string // ✅ Correction : Type explicite

  const api: AxiosInstance = axios.create({
    baseURL: apiBase
  })

  nuxtApp.provide('api', api) // Injecte $api dans Nuxt
})