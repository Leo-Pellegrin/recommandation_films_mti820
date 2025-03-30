import { ref, computed, onMounted, watch } from 'vue'

interface Actor {
  id: number
  name: string
  profilePath: string | null
}

// URLs TMDB
const TMDB_API_URL = 'https://api.themoviedb.org/3'
const TMDB_API_KEY = '166e544a3195c0c362b7c9294e90775d'

export function useActors() {
  const allActors = ref<Actor[]>([]) // ✅ typé
  const selectedActors = ref<Actor[]>([]) // ✅ typé
  const searchQuery = ref('')

  // 🔹 Charger les acteurs populaires
  async function fetchPopularActors() {
    try {
      const uniqueActors = new Map<number, Actor>()

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

      allActors.value = Array.from(uniqueActors.values())
    } catch (error) {
      console.error('Erreur lors de la récupération des acteurs:', error)
    }
  }

  // 🔹 Ajouter / retirer un acteur
  function toggleActor(actor: Actor) {
    const index = selectedActors.value.findIndex(a => a.id === actor.id)
    if (index > -1) {
      selectedActors.value.splice(index, 1)
    } else {
      selectedActors.value.push(actor)
    }
  }

  // 🔹 Recherche + filtrage
  const displayedActors = computed(() => {
    const filtered = allActors.value.filter(
      (actor) => !selectedActors.value.some(selected => selected.id === actor.id)
    )

    if (!searchQuery.value) return filtered.slice(0, 12)

    return filtered.filter((actor) =>
      actor.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    ).slice(0, 12)
  })

  // 🔹 Recherche via l'API TMDB
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

  // 🔹 Mode édition : récupérer des acteurs à partir de noms
  async function fetchActorsByNames(names: string[]) {
    try {
      const res = await fetch('http://localhost:8000/api/tools/actors/by-names', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ names })
      })

      const data = await res.json()
      selectedActors.value = (data.actors || []).map((actor: any) => ({
        id: actor.id,
        name: actor.name,
        profilePath: actor.profile_path ?? '/images/placeholder_actor.png'
      }))
    } catch (err) {
      console.error('Erreur lors de la récupération des acteurs :', err)
    }
  }

  // ✅ Init
  onMounted(fetchPopularActors)

  return {
    allActors,
    selectedActors,
    toggleActor,
    displayedActors,
    searchQuery,
    fetchActorsByNames
  }
}