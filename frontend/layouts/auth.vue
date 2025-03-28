<template>
  <div class="flex min-h-screen items-center justify-center bg-black">
    <div class="p-6 absolute top-0 left-0">
      <NuxtLink>
        <img src="/images/logo.svg" alt="MoodFlix Logo" class="w-50 h-50" />
      </NuxtLink>
    </div>
    <slot />
  </div>
</template>