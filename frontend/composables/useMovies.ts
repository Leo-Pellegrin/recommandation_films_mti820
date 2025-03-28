import { ref, computed, onMounted, watch } from 'vue'

interface Movie {
  id: number
  title: string
  posterPath?: string
}

export function useMovies() {
  const allMovies = ref<Movie[]>([])
  const selectedMovies = ref<Movie[]>([])
  const searchQuery = ref('')

  async function fetchMovies(limit = 20) {
    try {
      const response = await fetch(`http://localhost:8000/api/movies/?limit=${limit}`)
      const data = await response.json()      
      console.log(data)
      allMovies.value = data.map((movie: any) => ({
        id: movie.movie_id,
        title: movie.title,
        posterPath: movie.poster_path ?? '/images/placeholder_movie.jpeg'
      }))
    } catch (error) {
      console.error('Erreur lors de la récupération des films :', error)
    }
  }

  async function searchMovies(query: string) {
    try {
      const response = await fetch(`http://localhost:8000/api/movies/search/${encodeURIComponent(query)}`)
      const data = await response.json()
      allMovies.value = data.map((movie: any) => ({
        id: movie.movie_id,
        title: movie.title,
        posterPath: movie.poster_path ?? '/images/placeholder_movie.jpeg'
      }))
    } catch (error) {
      console.error('Erreur lors de la recherche de films :', error)
    }
  }

  function toggleMovie(movie: Movie) {
    const index = selectedMovies.value.findIndex(m => m.id === movie.id)
    if (index > -1) {
      selectedMovies.value.splice(index, 1)
    } else {
      selectedMovies.value.push(movie)
    }
  }

  const displayedMovies = computed(() => {
    const filtered = allMovies.value.filter(
      (movie) => !selectedMovies.value.some(selected => selected.id === movie.id)
    )
    return filtered.slice(0, 12)
  })

  watch(searchQuery, async (query) => {
    if (!query) {
      fetchMovies()
    } else {
      await searchMovies(query)
    }
  })

  onMounted(() => fetchMovies())

  return {
    allMovies,
    selectedMovies,
    toggleMovie,
    displayedMovies,
    fetchMovies,
    searchQuery
  }
}