import { ref, onMounted } from 'vue'
import { useUserStore } from '~/store/userStore'

interface Movie {
  id: number
  title: string
  posterPath: string
  genres: string[]
  preferenceScore: number // Score de recommandation
}

export function useTopRatedMovies() {
  const userStore = useUserStore()
  const topRatedMovies = ref<Movie[]>([])
  const loading = ref(true)

  async function fetchHybridRecommendations() {
    try {
      const userId = userStore.user?.id
      if (!userId) throw new Error("Utilisateur non connecté")

      const response = await fetch(`http://localhost:8000/api/recommendations/hybrid/${userId}`)
      const movies: Movie[] = await response.json()

      if (!movies.length) {
        topRatedMovies.value = []
        return
      }

      // Améliorer la qualité des images
      movies.forEach((movie) => {
        if (movie.posterPath?.includes('/w185')) {          
          movie.posterPath = movie.posterPath.replace('/w185', '/w500')
        }
        else {
          movie.posterPath = "/images/placeholder_movie.jpeg"
        }
      })


      // Trier les films par score décroissant
      topRatedMovies.value = movies.sort((a, b) => (b.preferenceScore ?? 0) - (a.preferenceScore ?? 0))

      console.log(topRatedMovies.value)
    } catch (e) {
      console.error('Erreur lors de la récupération des recommandations hybrides :', e)
    } finally {
      loading.value = false
    }
  }

  onMounted(fetchHybridRecommendations)

  return {
    topRatedMovies,
    loading
  }
}