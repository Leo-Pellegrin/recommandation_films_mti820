<template>
  <header class="bg-black p-4 flex justify-between items-center">
    <!-- Logo -->
    <NuxtLink to="/">
      <img src="/images/logo_header.svg" alt="MoodFlix Logo" class="w-50 h-50" />
    </NuxtLink>

    <!-- Navigation -->
    <nav class="space-x-6 hidden md:flex ml-auto text-xl border-2 border-gray-600 p-5 rounded-lg">
      <NuxtLink v-for="link in links" :key="link.to" :to="link.to" class="hover:scale-105 transition-all"
        :class="{ 'text-white font-bold': $route.path === link.to, 'text-gray-400 hover:text-white': $route.path !== link.to }">
        {{ link.label }}
      </NuxtLink>
    </nav>

    <!-- Icons (Alignés à droite) -->
    <nav class="flex items-center my-10 ml-auto mr-10">
      <UButton @click="openSearchModal" icon="line-md-search" size="xl"
        class="mx-2 text-white  hover:scale-115 transition-all text-xl">
      </UButton>
      <UButton icon="line-md-bell" size="xl" class="mx-2 text-white hover:scale-115 transition-all text-xl">
      </UButton>
      <UButton @click="navigateTo('/profile/preferences')" icon="line-md-account" size="xl" class="mx-2 text-white hover:scale-115 transition-all text-3xl">
        
      </UButton>
    </nav>
  </header>
</template>

<script setup>
import { SearchBar } from '#components'

// Définition des liens de navigation
const links = [
  { label: "Home", to: "/" },
  { label: "Movies", to: "/movies" },
  { label: "News and Popular", to: "/news" },
  { label: "Categories", to: "/categories" },
];


const overlay = useOverlay()

function openSearchModal() {
  const modal = overlay.create(SearchBar)

  modal.open()
}

</script>