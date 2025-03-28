// composables/useMovieCategories.ts
import { ref, onMounted } from 'vue'

interface Movie {
  id: number
  title: string
  posterPath: string
  genreIds: number[]
}

interface Genre {
  id: number
  name: string
}

const TMDB_AUTH_HEADER = {
  Authorization: `Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxNjZlNTQ0YTMxOTVjMGMzNjJiN2M5Mjk0ZTkwNzc1ZCIsIm5iZiI6MTYxMTkyMzU1NC4wMTMsInN1YiI6IjYwMTQwMDYyMTUxMWFhMDA0MDUwZTRiYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.eBu8apq8f56k4Ld1E8C3pqtN62bH3BMs2hrfjKzotQA`,
  Accept: 'application/json',
}
const TMDB_API_KEY = '166e544a3195c0c362b7c9294e90775d'

export function useTopRatedMovies() {
  const movieCategories = ref<Record<string, any[]>>({})
  const loading = ref(true)

  async function fetchGenres() {
    const res = await fetch('http://localhost:8000/api/movies/genres')
    const genres: string[] = await res.json()
    // Initialiser les catégories
    genres.slice(1).forEach((genre) => { // On ignore "(no genres listed)"
      movieCategories.value[genre] = []
    })
  }

  async function fetchMovies() {
    const allMovies: any[] = []
    for (let page = 1; page <= 20; page++) {
      const url = `https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=${page}&sort_by=vote_average.desc&without_genres=99,10755&vote_count.gte=200`

      const res = await fetch(url, { headers: TMDB_AUTH_HEADER })
      const data = await res.json()
      allMovies.push(...data.results)
    }

    return allMovies
  }

  async function organizeMoviesByGenre() {
    try {
      await fetchGenres()
      const movies = await fetchMovies()

      for (const movie of movies) {
        for (const genreId of movie.genre_ids) {
          // Appel à TMDB pour obtenir les noms des genres
          const genreName = await getGenreNameById(genreId)
          if (movieCategories.value[genreName]) {
            movieCategories.value[genreName].push({
              id: movie.id,
              title: movie.title,
              posterPath: movie.backdrop_path
                ? `https://image.tmdb.org/t/p/w780${movie.backdrop_path}`
                : '/images/placeholder_movie.jpeg',
              rating: movie.vote_average,
            })
          }
        }
      }

      for (const genre in movieCategories.value) {
        if (movieCategories.value[genre].length === 0) {
          delete movieCategories.value[genre]
        }
      }

    } catch (e) {
      console.error('Erreur lors du classement des films par genre', e)
    } finally {
      loading.value = false
    }
  }

  // Cette fonction mappe l'ID d'un genre à son nom
  const genreMapCache = new Map<number, string>()

  async function getGenreNameById(id: number): Promise<string> {
    if (genreMapCache.has(id)) return genreMapCache.get(id)!

    const res = await fetch(`https://api.themoviedb.org/3/genre/movie/list?language=en`, {
      headers: TMDB_AUTH_HEADER
    })
    const data = await res.json()
    for (const genre of data.genres) {
      genreMapCache.set(genre.id, genre.name)
    }
    return genreMapCache.get(id) || 'Unknown'
  }

  onMounted(organizeMoviesByGenre)

  return {
    movieCategories,
    loading
  }
}
