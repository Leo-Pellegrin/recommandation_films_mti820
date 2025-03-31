import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from '~/store/userStore'

const userStore = useUserStore()

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

  async function toggleMovie(movie: Movie) {
    const index = selectedMovies.value.findIndex(m => m.id === movie.id)

    if (index > -1) {
      // 🎯 Le film est déjà sélectionné, on le supprime localement + en base
      selectedMovies.value.splice(index, 1)

      const userId = userStore.user?.id
      if (!userId) return

      try {
        const res = await fetch(`http://localhost:8000/api/preferences/${userId}/favorites/movies/${movie.id}`, {
          method: 'DELETE',
        })

        if (!res.ok) {
          const error = await res.json()
          console.error('Erreur lors de la suppression du film en base :', error.detail)
        }
      } catch (err) {
        console.error('Erreur réseau lors de la suppression du film :', err)
      }
    } else {
      // ➕ Ajout local uniquement
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