<script setup lang="ts">
import type { FormSubmitEvent, FormError } from '@nuxt/ui'
import { useUserStore } from '~/store/userStore'

const router = useRouter()

const userStore = useUserStore()
definePageMeta({
  middleware: 'guest',
  layout: 'auth'
})

// État réactif du formulaire
const state = reactive({
  email: '',
  password: ''
})

// Fonction de validation manuelle
const validate = (state: any): FormError[] => {
  const errors: FormError[] = []

  if (!state.email) {
    errors.push({ name: 'email', message: 'Email is required' })
  } else if (!/\S+@\S+\.\S+/.test(state.email)) {
    errors.push({ name: 'email', message: 'Invalid email format' })
  }

  if (!state.password) {
    errors.push({ name: 'password', message: 'Password is required' })
  }

  return errors
}

// Toast notifications
const toast = useToast()
const loading = ref(false)

// Soumission du formulaire
async function onSubmit(event: FormSubmitEvent<any>) {
  loading.value = true;

  try {
    const formData = new URLSearchParams();
    formData.append("username", state.email.trim());
    formData.append("password", state.password);

    const response = await fetch("http://localhost:8000/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formData
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Login failed. Please try again.");
    }
    
    const token = useCookie('auth.token')
    token.value = data.access_token

    userStore.login({
      id: data.id,
      email: data.email,
      username: data.username,
    });

    console.log("Login successful:", data);
    if (data.first_login) {
      console.log("Premier login")
      window.location.href = '/onboarding/genres'
    } 
    // else {
    //   window.location.reload() // Recharger la page actuelle
    // }

  } catch (error: any) {
    console.error("Erreur de connexion :", error);
    toast.add({ title: "Error", description: error.message || "Login failed", color: "error" });

  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <UCard class="max-w-2xl mx-auto bg-gray-200 border-2 border-gray-600 p-12 rounded-3xl shadow-2xl">
    <template #header>
      <h2 class="text-4xl font-extrabold text-left text-black">Sign In</h2>
    </template>

    <UForm :validate="validate" :state="state" class="space-y-8" @submit="onSubmit">
      <UFormField label="Email" name="username" class="w-full text-3xl mt-6">
        <UInput v-model="state.email" placeholder="Enter your email" size="xl" :ui="{ base: 'px-6 py-4 text-xl rounded-xl' }" 
          class="w-full mt-4 rounded-2xl" />
      </UFormField>

      <UFormField label="Password" name="password" class="w-full text-3xl">
        <UInput v-model="state.password" type="password" placeholder="Enter your password" size="xl"   :ui="{ base: 'px-6 py-4 text-xl rounded-xl' }" 
          class="w-full mt-4 rounded-2xl" />
      </UFormField>

      <UButton type="submit" block :loading="loading" size="xl"
        class="mt-6 py-2 text-2xl font-bold rounded-2xl bg-orange-400 hover:bg-orange-600 transition-all">
        Sign In
      </UButton>
    </UForm>

    <p class="text-center text-2xl text-black mt-6">
      Don't have an account?
      <NuxtLink to="/auth/register" class="text-orange-600 hover:underline text-2xl font-semibold">Sign Up today !
      </NuxtLink>
    </p>
  </UCard>
</template>