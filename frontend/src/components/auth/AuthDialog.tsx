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

interface AuthDialogProps {
  mode?: "signin" | "signup"
  trigger?: React.ReactNode
}

export function AuthDialog({ mode = "signin", trigger }: AuthDialogProps) {
  const [isSignIn, setIsSignIn] = useState(mode === "signin")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [name, setName] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // TODO: Implement authentication logic
    console.log({ email, password, name })
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
            <div className="space-y-2">
              <Label htmlFor="name">Name</Label>
              <Input
                id="name"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
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
