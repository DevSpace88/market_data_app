<!--// src/components/Auth.vue-->
<!--<script setup>-->
<!--import { ref, computed } from 'vue'-->
<!--import axios from 'axios'-->
<!--import { useToast } from '@/components/ui/toast/use-toast'-->
<!--import { Button } from '@/components/ui/button'-->
<!--import {-->
<!--  Card,-->
<!--  CardContent,-->
<!--  CardDescription,-->
<!--  CardFooter,-->
<!--  CardHeader,-->
<!--  CardTitle,-->
<!--} from '@/components/ui/card'-->
<!--import { Input } from '@/components/ui/input'-->
<!--import { Label } from '@/components/ui/label'-->
<!--import {-->
<!--  Tabs,-->
<!--  TabsContent,-->
<!--  TabsList,-->
<!--  TabsTrigger,-->
<!--} from '@/components/ui/tabs'-->

<!--const API_URL = 'http://localhost:8000/api/v1/auth'-->
<!--const { toast } = useToast()-->

<!--const username = ref('')-->
<!--const email = ref('')-->
<!--const password = ref('')-->
<!--const fullName = ref('')-->
<!--const user = ref(null)-->
<!--const isLoggedIn = ref(false)-->
<!--const isLoading = ref(false)-->

<!--const clearForm = () => {-->
<!--  username.value = ''-->
<!--  email.value = ''-->
<!--  password.value = ''-->
<!--  fullName.value = ''-->
<!--}-->

<!--const register = async () => {-->
<!--  try {-->
<!--    isLoading.value = true-->
<!--    const response = await axios.post(`${API_URL}/register`, {-->
<!--      username: username.value,-->
<!--      email: email.value,-->
<!--      password: password.value,-->
<!--      full_name: fullName.value-->
<!--    })-->

<!--    toast({-->
<!--      title: 'Registration successful',-->
<!--      description: 'Please login with your new account',-->
<!--    })-->

<!--    clearForm()-->
<!--  } catch (err) {-->
<!--    toast({-->
<!--      title: 'Registration failed',-->
<!--      description: err.response?.data?.detail || 'Something went wrong',-->
<!--      variant: 'destructive',-->
<!--    })-->
<!--  } finally {-->
<!--    isLoading.value = false-->
<!--  }-->
<!--}-->

<!--const login = async () => {-->
<!--  try {-->
<!--    isLoading.value = true-->
<!--    const formData = new FormData()-->
<!--    formData.append('username', username.value)-->
<!--    formData.append('password', password.value)-->

<!--    const response = await axios.post(`${API_URL}/login`, formData)-->
<!--    const { access_token, user: userData } = response.data-->

<!--    localStorage.setItem('token', access_token)-->
<!--    user.value = userData-->
<!--    isLoggedIn.value = true-->

<!--    axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`-->

<!--    toast({-->
<!--      title: 'Login successful',-->
<!--      description: `Welcome back, ${userData.username}!`,-->
<!--    })-->

<!--    clearForm()-->
<!--  } catch (err) {-->
<!--    toast({-->
<!--      title: 'Login failed',-->
<!--      description: err.response?.data?.detail || 'Invalid credentials',-->
<!--      variant: 'destructive',-->
<!--    })-->
<!--  } finally {-->
<!--    isLoading.value = false-->
<!--  }-->
<!--}-->

<!--const logout = async () => {-->
<!--  try {-->
<!--    await axios.post(`${API_URL}/logout`)-->
<!--    toast({-->
<!--      title: 'Logged out',-->
<!--      description: 'You have been successfully logged out',-->
<!--    })-->
<!--  } catch (err) {-->
<!--    console.error('Logout error:', err)-->
<!--  } finally {-->
<!--    localStorage.removeItem('token')-->
<!--    user.value = null-->
<!--    isLoggedIn.value = false-->
<!--    delete axios.defaults.headers.common['Authorization']-->
<!--  }-->
<!--}-->

<!--const checkAuth = async () => {-->
<!--  const token = localStorage.getItem('token')-->
<!--  if (token) {-->
<!--    try {-->
<!--      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`-->
<!--      const response = await axios.get(`${API_URL}/me`)-->
<!--      user.value = response.data-->
<!--      isLoggedIn.value = true-->
<!--    } catch (err) {-->
<!--      localStorage.removeItem('token')-->
<!--      delete axios.defaults.headers.common['Authorization']-->
<!--    }-->
<!--  }-->
<!--}-->

<!--checkAuth()-->
<!--</script>-->

<!--<template>-->
<!--  <div class="flex justify-center items-center min-h-screen bg-background">-->
<!--    <Card class="w-[350px]" v-if="!isLoggedIn">-->
<!--      <CardHeader>-->
<!--        <CardTitle>Account</CardTitle>-->
<!--        <CardDescription>-->
<!--          Manage your account-->
<!--        </CardDescription>-->
<!--      </CardHeader>-->
<!--      <CardContent>-->
<!--        <Tabs default-value="login" class="w-full">-->
<!--          <TabsList class="grid w-full grid-cols-2">-->
<!--            <TabsTrigger value="login">Login</TabsTrigger>-->
<!--            <TabsTrigger value="register">Register</TabsTrigger>-->
<!--          </TabsList>-->

<!--          &lt;!&ndash; Login Tab &ndash;&gt;-->
<!--          <TabsContent value="login">-->
<!--            <form @submit.prevent="login">-->
<!--              <div class="grid gap-4">-->
<!--                <div class="grid gap-2">-->
<!--                  <Label for="username">Username</Label>-->
<!--                  <Input-->
<!--                    id="username"-->
<!--                    v-model="username"-->
<!--                    placeholder="your username"-->
<!--                    required-->
<!--                  />-->
<!--                </div>-->
<!--                <div class="grid gap-2">-->
<!--                  <Label for="password">Password</Label>-->
<!--                  <Input-->
<!--                    id="password"-->
<!--                    type="password"-->
<!--                    v-model="password"-->
<!--                    placeholder="your password"-->
<!--                    required-->
<!--                  />-->
<!--                </div>-->
<!--                <Button type="submit" :disabled="isLoading">-->
<!--                  {{ isLoading ? 'Loading...' : 'Login' }}-->
<!--                </Button>-->
<!--              </div>-->
<!--            </form>-->
<!--          </TabsContent>-->

<!--          &lt;!&ndash; Register Tab &ndash;&gt;-->
<!--          <TabsContent value="register">-->
<!--            <form @submit.prevent="register">-->
<!--              <div class="grid gap-4">-->
<!--                <div class="grid gap-2">-->
<!--                  <Label for="reg-username">Username</Label>-->
<!--                  <Input-->
<!--                    id="reg-username"-->
<!--                    v-model="username"-->
<!--                    placeholder="choose username"-->
<!--                    required-->
<!--                  />-->
<!--                </div>-->
<!--                <div class="grid gap-2">-->
<!--                  <Label for="email">Email</Label>-->
<!--                  <Input-->
<!--                    id="email"-->
<!--                    type="email"-->
<!--                    v-model="email"-->
<!--                    placeholder="your email"-->
<!--                    required-->
<!--                  />-->
<!--                </div>-->
<!--                <div class="grid gap-2">-->
<!--                  <Label for="reg-password">Password</Label>-->
<!--                  <Input-->
<!--                    id="reg-password"-->
<!--                    type="password"-->
<!--                    v-model="password"-->
<!--                    placeholder="choose password"-->
<!--                    required-->
<!--                  />-->
<!--                </div>-->
<!--                <div class="grid gap-2">-->
<!--                  <Label for="fullName">Full Name</Label>-->
<!--                  <Input-->
<!--                    id="fullName"-->
<!--                    v-model="fullName"-->
<!--                    placeholder="your full name"-->
<!--                  />-->
<!--                </div>-->
<!--                <Button type="submit" :disabled="isLoading">-->
<!--                  {{ isLoading ? 'Loading...' : 'Register' }}-->
<!--                </Button>-->
<!--              </div>-->
<!--            </form>-->
<!--          </TabsContent>-->
<!--        </Tabs>-->
<!--      </CardContent>-->
<!--    </Card>-->

<!--    &lt;!&ndash; Logged In State &ndash;&gt;-->
<!--    <Card class="w-[350px]" v-else>-->
<!--      <CardHeader>-->
<!--        <CardTitle>Welcome back!</CardTitle>-->
<!--        <CardDescription>-->
<!--          You are logged in as {{ user?.username }}-->
<!--        </CardDescription>-->
<!--      </CardHeader>-->
<!--      <CardContent>-->
<!--        <div class="space-y-2">-->
<!--          <p class="text-sm text-muted-foreground">-->
<!--            Email: {{ user?.email }}-->
<!--          </p>-->
<!--          <p class="text-sm text-muted-foreground" v-if="user?.full_name">-->
<!--            Full Name: {{ user?.full_name }}-->
<!--          </p>-->
<!--        </div>-->
<!--      </CardContent>-->
<!--      <CardFooter>-->
<!--        <Button @click="logout" class="w-full" variant="destructive">-->
<!--          Logout-->
<!--        </Button>-->
<!--      </CardFooter>-->
<!--    </Card>-->
<!--  </div>-->
<!--</template>-->


<template>
  <div class="flex justify-center items-center min-h-screen bg-background">
    <Card class="w-[350px]" v-if="!authStore.isAuthenticated">
      <CardHeader>
        <CardTitle>Account</CardTitle>
        <CardDescription>
          Manage your account
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs default-value="login" class="w-full">
          <TabsList class="grid w-full grid-cols-2">
            <TabsTrigger value="login">Login</TabsTrigger>
            <TabsTrigger value="register">Register</TabsTrigger>
          </TabsList>
          <TabsContent value="login">
            <form @submit.prevent="handleLogin">
              <div class="grid gap-4">
                <div class="grid gap-2">
                  <Label for="username">Username</Label>
                  <Input
                    id="username"
                    v-model="loginForm.username"
                    placeholder="your username"
                    required
                  />
                </div>
                <div class="grid gap-2">
                  <Label for="password">Password</Label>
                  <Input
                    id="password"
                    type="password"
                    v-model="loginForm.password"
                    placeholder="your password"
                    required
                  />
                </div>
                <Button type="submit" :disabled="authStore.loading">
                  {{ authStore.loading ? 'Loading...' : 'Login' }}
                </Button>
              </div>
            </form>
          </TabsContent>
          <TabsContent value="register">
            <form @submit.prevent="handleRegister">
              <div class="grid gap-4">
                <div class="grid gap-2">
                  <Label for="reg-username">Username</Label>
                  <Input
                    id="reg-username"
                    v-model="registerForm.username"
                    placeholder="choose username"
                    required
                  />
                </div>
                <div class="grid gap-2">
                  <Label for="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    v-model="registerForm.email"
                    placeholder="your email"
                    required
                  />
                </div>
                <div class="grid gap-2">
                  <Label for="reg-password">Password</Label>
                  <Input
                    id="reg-password"
                    type="password"
                    v-model="registerForm.password"
                    placeholder="choose password"
                    required
                  />
                </div>
                <div class="grid gap-2">
                  <Label for="fullName">Full Name</Label>
                  <Input
                    id="fullName"
                    v-model="registerForm.fullName"
                    placeholder="your full name"
                  />
                </div>
                <Button type="submit" :disabled="authStore.loading">
                  {{ authStore.loading ? 'Loading...' : 'Register' }}
                </Button>
              </div>
            </form>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
    <Card class="w-[350px]" v-else>
      <CardHeader>
        <CardTitle>Welcome back!</CardTitle>
        <CardDescription>
          You are logged in as {{ authStore.user?.username }}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div class="space-y-2">
          <p class="text-sm text-muted-foreground">
            Email: {{ authStore.user?.email }}
          </p>
          <p class="text-sm text-muted-foreground" v-if="authStore.user?.full_name">
            Full Name: {{ authStore.user?.full_name }}
          </p>
          <p class="text-sm text-muted-foreground">
            Member since: {{ formatDate(authStore.user?.created_at) }}
          </p>
        </div>
      </CardContent>
      <CardFooter>
        <Button @click="handleLogout" class="w-full" variant="destructive">
          Logout
        </Button>
      </CardFooter>
    </Card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/components/ui/toast/use-toast'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs'

const authStore = useAuthStore()
const { toast } = useToast()

const loginForm = ref({
  username: '',
  password: ''
})

const registerForm = ref({
  username: '',
  email: '',
  password: '',
  fullName: ''
})

const handleLogin = async () => {
  const success = await authStore.login(
    loginForm.value.username,
    loginForm.value.password
  )

  if (success) {
    toast({
      title: "Success",
      description: "Successfully logged in",
    })
  } else {
    toast({
      title: "Error",
      description: authStore.error || "Login failed",
      variant: "destructive",
    })
  }
}

const handleRegister = async () => {
  const success = await authStore.register(registerForm.value)

  if (success) {
    toast({
      title: "Success",
      description: "Registration successful",
    })
  } else {
    toast({
      title: "Error",
      description: authStore.error || "Registration failed",
      variant: "destructive",
    })
  }
}

const handleLogout = () => {
  authStore.logout()
  toast({
    title: "Success",
    description: "Successfully logged out",
  })
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>