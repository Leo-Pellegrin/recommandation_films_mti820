import type { AxiosInstance } from 'axios'

interface Movie {
  id: number
  title: string
  poster: string
  rating: number
}

export function useFetchMovies(): { movies: Ref<Movie[]>; fetchMovies: () => Promise<void> } {
  const movies = ref<Movie[]>([])

  async function fetchMovies() {
    const { $api } = useNuxtApp() as unknown as { $api: AxiosInstance }
    try {
      const response = await $api.get('/movies')
      movies.value = response.data
    } catch (error) {
      console.error('Erreur lors de la récupération des films', error)
    }
  }

  return { movies, fetchMovies }
}