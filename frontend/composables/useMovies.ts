// composables/useMovies.ts
import { ref, computed, onMounted } from 'vue'

interface Movie {
  id: number
  title: string
  posterPath: string | undefined
}

const TMDB_API_URL = 'https://api.themoviedb.org/3'
const TMDB_API_KEY = '166e544a3195c0c362b7c9294e90775d'

export function useMovies() {
  const allMovies = ref<Movie[]>([])
  const selectedMovies = ref<Movie[]>([])
  const searchQuery = ref('')

  async function fetchPopularMovies() {
    try {
      const uniqueMovies = new Map()

      for (let page = 1; page <= 5; page++) {
        const response = await fetch(`${TMDB_API_URL}/movie/popular?api_key=${TMDB_API_KEY}&language=en-US&page=${page}`)
        const data = await response.json()

        console.log("data", data)
        if (data.results) {
          for (const movie of data.results) {
            if (!uniqueMovies.has(movie.id)) {
              uniqueMovies.set(movie.id, {
                id: movie.id,
                title: movie.title,
                posterPath: movie.poster_path
                  ? `https://image.tmdb.org/t/p/w185${movie.poster_path}`
                  : '/images/placeholder_movie.jpeg'
              })
            }
          }
        }
      }

      allMovies.value = Array.from(uniqueMovies.values())

    } catch (error) {
      console.error('Erreur lors de la récupération des films:', error)
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
    ).slice(0, 12)


    const searched = searchQuery.value
      ? filtered.filter((movie) => movie.title.toLowerCase().includes(searchQuery.value.toLowerCase()))
      : filtered

    return searched.slice(0, 12)
  })


  watch(searchQuery, async (query) => {
    if (!query) {
      fetchPopularMovies()
      return
    }

    try {
      const response = await fetch(`${TMDB_API_URL}/search/movie?api_key=${TMDB_API_KEY}&query=${encodeURIComponent(query)}&language=en-US&page=1`)
      const data = await response.json()

      if (data.results) {
        allMovies.value = data.results
          .map((movie: any) => ({
            id: movie.id,
            title: movie.title,
            posterPath: movie.poster_path
              ? `https://image.tmdb.org/t/p/w185${movie.poster_path}`
              : '/images/placeholder_movie.jpeg'
          }))
      }
    } catch (error) {
      console.error('Erreur de recherche TMDB :', error)
    }
  })

  onMounted(fetchPopularMovies)

  return {
    allMovies,
    selectedMovies,
    toggleMovie,
    displayedMovies,
    fetchPopularMovies,
    searchQuery
  }

}


