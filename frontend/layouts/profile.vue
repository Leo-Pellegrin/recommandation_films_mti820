<script setup lang="ts">
const route = useRoute()

watchEffect(() => {
  console.log(route.path)
})

const isActive = (to: string) => {
  return route.path === to || route.path.startsWith(to + '/')
}

const items = computed(() => [
  {
    label: 'General',
    defaultOpen: true,
    class: 'text-3xl',
    children: [
      {
        label: 'Notifications',
        icon: 'i-lucide-bell',
        to: '/profile/preferences',
        class: isActive('/profile/notifications') ? 'text-orange-500 font-bold text-xl' : 'text-white text-xl',
      },
      {
        label: 'Preferences',
        icon: 'i-lucide-heart',
        to: '/profile/preferences',
        class: isActive('/profile/preferences') ? 'text-orange-500 font-bold text-xl' : 'text-white text-xl',
      },
      {
        label: 'Membership',
        icon: 'i-lucide-credit-card',
        to: '/profile/preferences',
        class: isActive('/profile/membership') ? 'text-orange-500 font-bold text-xl' : 'text-white text-xl',
      },
    ],
  },
  {
    label: 'Ratings',
    defaultOpen: true,
    class: 'text-3xl',
    children: [
      {
        label: 'Historique',
        icon: 'i-lucide-history',
        to: '/profile/ratings',
        class: isActive('/profile/ratings') ? 'text-orange-500 font-bold text-xl' : 'text-white text-xl'
      },
    ],
  }
])
</script>

<template>
  <AppBar />
  <div class="min-h-screen flex bg-black text-white">
    <!-- Sidebar -->
    <aside class="w-70 p-6 border-r border-gray-800">
      <h2 class="text-3xl font-bold mb-6">Account settings</h2>
      <UNavigationMenu highlight color="primary" highlight-color="primary" orientation="vertical" :items="items"
        class="data-[orientation=vertical]:w-55" />
    </aside>

    <!-- Main Content -->
    <main class="flex-1 p-10 bg-[#f2f2f2] text-black rounded-tl-3xl">
      <slot />
    </main>
  </div>
</template>

<style scoped>
</style>