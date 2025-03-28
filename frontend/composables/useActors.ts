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

  // Récupérer les acteurs populaires depuis TMDB
  async function fetchPopularActors() {
    try {
      const uniqueActors = new Map()

      // 🔁 Boucle sur les pages 1 à 5 (ajuste si besoin)
      for (let page = 1; page <= 5; page++) {
        const response = await fetch(`${TMDB_API_URL}/person/popular?api_key=${TMDB_API_KEY}&language=en-US&page=${page}`)
        const data = await response.json()

        if (data.results) {
          for (const actor of data.results) {
            if (!uniqueActors.has(actor.id) && actor.known_for_department === 'Acting') {
              uniqueActors.set(actor.id, {
                id: actor.id,
                name: actor.name,
                profilePath: actor.profile_path
                  ? `https://image.tmdb.org/t/p/w185${actor.profile_path}`
                  : '/images/placeholder_actor.png'
              })
            }
          }
        }
      }

      // Stocker les acteurs uniques
      allActors.value = Array.from(uniqueActors.values())
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

  const displayedActors = computed(() => {
    const filtered = allActors.value.filter(
      (actor) => !selectedActors.value.some(selected => selected.id === actor.id)
    )

    if (!searchQuery.value) {
      //Toujours limiter à 12 en l'absence de recherche
      return filtered.slice(0, 12)
    }

    // En cas de recherche, ne pas tronquer à 12 pour voir tous les résultats correspondants
    return filtered.filter((actor) =>
      actor.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    ).slice(0, 12)
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
        allActors.value = data.results
          .filter((actor: any) => actor.known_for_department === 'Acting')
          .map((actor: any) => ({
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