import { useState } from "react"
import { Button } from "../ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "../ui/dialog"
import { Input } from "../ui/input"
import { Label } from "../ui/label"
import { toast } from "../ui/use-toast"

interface AuthDialogProps {
  mode?: "signin" | "signup"
  trigger?: React.ReactNode
}

export function AuthDialog({ mode = "signin", trigger }: AuthDialogProps) {
  const [isSignIn, setIsSignIn] = useState(mode === "signin")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [username, setUsername] = useState("")
  const [fullName, setFullName] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const endpoint = `${import.meta.env.VITE_API_URL}/auth/${isSignIn ? 'login' : 'register'}`
      
      const response = await (async () => {
        if (isSignIn) {
          // Login: Use URL-encoded format for OAuth2
          const formBody = new URLSearchParams()
          formBody.append('username', email) // OAuth2 expects 'username' field
          formBody.append('password', password)
          
          return await fetch(endpoint, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
              'Accept': 'application/json',
            },
            credentials: 'include',
            body: formBody,
          })
        } else {
          // Register: Use JSON format
          return await fetch(endpoint, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({
              email,
              password,
              username,
              full_name: fullName,
            }),
          })
        }
      })()

      const data = await response.json()
      if (!response.ok) {
        throw new Error(data.detail || 'Authentication failed')
      }

      if (isSignIn) {
        localStorage.setItem('token', data.access_token)
      }
      
      toast({
        title: isSignIn ? "Welcome back!" : "Account created",
        description: isSignIn ? "Successfully signed in" : "Please check your email to verify your account",
      })
      
      if (isSignIn) {
        window.location.reload()
      }

    } catch (error) {
      console.error('Authentication error:', error)
      toast({
        title: "Authentication failed",
        description: error instanceof Error ? error.message : "Please try again",
        variant: "destructive",
      })
    }
  }

  return (
    <Dialog>
      <DialogTrigger asChild>
        {trigger || (
          <Button variant={isSignIn ? "ghost" : "default"}>
            {isSignIn ? "Sign In" : "Sign Up"}
          </Button>
        )}
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>{isSignIn ? "Sign In" : "Create Account"}</DialogTitle>
          <DialogDescription>
            {isSignIn
              ? "Enter your credentials to access your account"
              : "Fill in your details to create a new account"}
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          {!isSignIn && (
            <>
              <div className="space-y-2">
                <Label htmlFor="username">Username</Label>
                <Input
                  id="username"
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="fullName">Full Name</Label>
                <Input
                  id="fullName"
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  required
                />
              </div>
            </>
          )}
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="flex flex-col space-y-4">
            <Button type="submit">
              {isSignIn ? "Sign In" : "Create Account"}
            </Button>
            <Button
              type="button"
              variant="ghost"
              onClick={() => setIsSignIn(!isSignIn)}
            >
              {isSignIn
                ? "Don't have an account? Sign Up"
                : "Already have an account? Sign In"}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  )
}
