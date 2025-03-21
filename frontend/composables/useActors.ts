import { ref, computed, onMounted } from 'vue'

interface Actor {
  id: number
  name: string
  profilePath: string | null
}

// URL de base TMDB
const TMDB_API_URL = 'https://api.themoviedb.org/3'
const TMDB_API_KEY = '166e544a3195c0c362b7c9294e90775d'

export function useActors() {
  const allActors = ref<any[]>([]) // Tous les acteurs récupérés
  const selectedActors = ref<any[]>([]) // Acteurs sélectionnés
  const searchQuery = ref('') // Recherche d'acteurs

  // 🔹 Récupérer les acteurs populaires depuis TMDB
  async function fetchPopularActors() {
    try {
      const response = await fetch(`${TMDB_API_URL}/person/popular?api_key=${TMDB_API_KEY}&language=en-US&spage=1`)
      const data = await response.json()

      // Vérifier si results existe avant d'appliquer filter
      if (data.results) {
        allActors.value = data.results.map((actor: any) => ({
          id: actor.id,
          name: actor.name,
          profilePath: actor.profile_path
            ? `https://image.tmdb.org/t/p/w185${actor.profile_path}`
            : '/images/placeholder_actor.png' // Image par défaut si absente
        }))
      } else {
        console.error('Erreur: TMDB ne retourne aucun acteur')
      }
    } catch (error) {
      console.error('Erreur lors de la récupération des acteurs:', error)
    }
  }

  function toggleActor(actor: Actor) {
    const index = selectedActors.value.findIndex(a => a.id === actor.id)
    if (index > -1) {
      selectedActors.value.splice(index, 1)
    } else {
      selectedActors.value.push(actor)
    }
  }
  // Acteurs affichés en fonction de la recherche, sans les sélectionnés
  const displayedActors = computed(() => {
    const filtered = allActors.value.filter(
      (actor) => !selectedActors.value.some(selected => selected.id === actor.id)
    )

    if (!searchQuery.value) return filtered
    return filtered.filter((actor) =>
      actor.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  })

  watch(searchQuery, async (query) => {
  if (!query) {
    fetchPopularActors()
    return
  }

  try {
    const response = await fetch(`${TMDB_API_URL}/search/person?api_key=${TMDB_API_KEY}&query=${encodeURIComponent(query)}&language=en-US&page=1`)
    const data = await response.json()

    if (data.results) {
      allActors.value = data.results.map((actor: any) => ({
        id: actor.id,
        name: actor.name,
        profilePath: actor.profile_path
          ? `https://image.tmdb.org/t/p/w185${actor.profile_path}`
          : '/images/placeholder_actor.png'
      }))
    }
  } catch (error) {
    console.error('Erreur de recherche TMDB :', error)
  }
})

  // 🔹 Charger les acteurs populaires au montage
  onMounted(fetchPopularActors)

  return {
    allActors,
    selectedActors,
    toggleActor,
    displayedActors,
    searchQuery
  }
}