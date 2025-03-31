import { ref, onMounted } from 'vue'
import { useUserStore } from '~/store/userStore'

interface Movie {
  id: number
  title: string
  posterPath: string
  genres: string[]
  rating: number // ici : score de recommandation
}

export function useTopRatedMovies() {
  const userStore = useUserStore()
  const movieCategories = ref<Record<string, Movie[]>>({})
  const loading = ref(true)

  async function fetchHybridRecommendations() {
    try {
      const userId = userStore.user?.id
      if (!userId) throw new Error("Utilisateur non connecté")

      const response = await fetch(`http://localhost:8000/api/recommendations/hybrid/${userId}`)
      console.log(response.json())
      const movies: Movie[] = await response.json()
      console.log(movies)

      if (!movies.length) {
        movieCategories.value = {}
        return
      }

      // Améliorer la qualité des images
      movies.forEach((movie) => {
        if (movie.posterPath?.includes('/w185')) {
          movie.posterPath = movie.posterPath.replace('/w185', '/w500')
        }
      })

      const ratings = movies.map((m) => m.rating ?? 0)
      const maxRating = Math.max(...ratings)
      const minRating = Math.min(...ratings)
      const range = (maxRating - minRating) / 3

      const buckets: Record<string, Movie[]> = {
        '🟢 Highly Recommended': [],
        '🟡 Moderately Recommended': [],
        '🔴 Less Relevant': []
      }

      for (const movie of movies) {
        const score = movie.rating ?? 0

        if (score >= minRating + 2 * range) {
          buckets['🟢 Highly Recommended'].push(movie)
        } else if (score >= minRating + range) {
          buckets['🟡 Moderately Recommended'].push(movie)
        } else {
          buckets['🔴 Less Relevant'].push(movie)
        }
      }

      movieCategories.value = buckets
      console.log(movieCategories.value)
    } catch (e) {
      console.error('Erreur lors de la récupération des recommandations hybrides :', e)
    } finally {
      loading.value = false
    }
  }

  onMounted(fetchHybridRecommendations)

  return {
    movieCategories,
    loading
  }
}