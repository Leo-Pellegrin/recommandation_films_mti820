<script setup lang="ts">
import type { FormSubmitEvent, FormError } from '@nuxt/ui'

definePageMeta({
  layout: 'auth',
  middleware: 'guest'
})

// État réactif du formulaire
const state = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// Vérification des erreurs
const validate = (state: Record<string, string>): FormError[] => {
  const errors: FormError[] = []

  if (!state.name.trim()) errors.push({ name: 'name', message: 'Name is required' })

  if (!state.email.trim()) {
    errors.push({ name: 'email', message: 'Email is required' })
  } else if (!/\S+@\S+\.\S+/.test(state.email)) {
    errors.push({ name: 'email', message: 'Invalid email format' })
  }

  if (!state.password) {
    errors.push({ name: 'password', message: 'Password is required' })
  } else if (state.password.length < 8) {
    errors.push({ name: 'password', message: 'Password must be at least 8 characters' })
  }

  if (state.password !== state.confirmPassword) {
    errors.push({ name: 'confirmPassword', message: 'Passwords do not match' })
  }

  return errors
}

// Toast notifications & loading state
const toast = useToast()
const loading = ref(false)

// Fonction de soumission
async function onSubmit(event: FormSubmitEvent<any>) {
  loading.value = true

  try {
    if (state.password !== state.confirmPassword) {
      toast.add({ title: 'Error', description: 'Passwords do not match', color: 'error' })
      return
    }

    const response = await fetch("http://localhost:8000/api/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username: state.name.trim(),
        email: state.email.trim(),
        password: state.password
      })
    })

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Registration failed. Please try again.");
    }

    if (data.id) {
      toast.add({ title: 'Success', description: 'Account created! Redirecting...', color: 'success' })
      setTimeout(() => {
        navigateTo('/auth/login')
        toast.clear()
      }, 3000);

    }

  } catch (error: any) {
    console.error('❌ Registration error:', error)
    let message = 'Registration failed. Please try again.'

    // Si l'API FastAPI renvoie un message d'erreur, on l'affiche
    if (error.message) {
      message = error.message
    }

    toast.add({ title: 'Error', description: message, color: 'error' })
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <UCard class="max-w-2xl mx-auto bg-gray-200 border-2 border-gray-600 p-12 rounded-3xl shadow-2xl">
    <template #header>
      <h2 class="text-4xl font-extrabold text-left text-black">Sign Up</h2>
    </template>

    <UForm :validate="validate" :state="state" class="space-y-8" @submit="onSubmit">
      <UFormField label="Full Name" name="name" class="w-full text-2xl mt-6 formfield">
        <UInput v-model="state.name" placeholder="Enter your full name" size="xl"
          :ui="{ base: 'px-6 py-4 text-lg rounded-xl' }" class="mt-4 w-full rounded-2xl" />
      </UFormField>

      <UFormField label="Email address" name="email" class="w-full text-2xl">
        <UInput v-model="state.email" type="email" placeholder="Enter your email" size="xl"
          :ui="{ base: 'px-6 py-4 text-xl rounded-xl' }" class=" mt-4 w-full  rounded-2xl" />
      </UFormField>

      <UFormField label="Password" name="password" class="w-full text-2xl">
        <UInput v-model="state.password" type="password" placeholder="Enter your password" size="xl"
          :ui="{ base: 'px-6 py-4 text-xl rounded-xl' }" class="mt-4 w-full rounded-2xl" />
      </UFormField>

      <UFormField label="Confirm Password" name="confirmPassword" class="w-full text-2xl">
        <UInput v-model="state.confirmPassword" type="password" placeholder="Confirm your password" size="xl"
          :ui="{ base: 'px-6 py-4 text-xl rounded-xl' }" class="mt-4 w-full rounded-2xl" />
      </UFormField>

      <UButton type="submit" block :loading="loading" size="xl"
        class="py-2 text-2xl font-bold rounded-2xl bg-orange-400 hover:bg-orange-600 transition-all">
        Sign Up
      </UButton>
    </UForm>

    <p class="text-center text-2xl text-black mt-6">
      Already have an account?
      <NuxtLink to="/auth/login" class="text-orange-600 hover:underline text-2xl font-semibold">
        Sign in now!
      </NuxtLink>
    </p>
  </UCard>
</template>

<style scoped>
/* Styles scopés pour les messages d'erreur dans ce composant */
.u-form-field p {
  font-size: 1.25rem;
  color: #e53e3e;
  font-weight: bold;
}
</style>