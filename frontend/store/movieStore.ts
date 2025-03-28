interface Movie {
  id: number
  title: string
  poster: string
  rating: number
}

export const useMovieStore = defineStore('movie', {
  state: () => ({
    movies: [] as Movie[],
  }),
  actions: {
    async fetchMovies() {
      // const { $api } = useNuxtApp()
      // try {
      //   const response = await $api.get<Movie[]>('/movies')
      //   this.movies = response.data
      // } catch (error) {
      //   console.error('Erreur lors de la récupération des films', error)
      // }
    },
  },
})