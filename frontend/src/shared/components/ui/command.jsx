import * as React from "react"
import { Dialog, DialogContent } from "@radix-ui/react-dialog"
import { cn } from "@/lib/utils"
import { Search } from "lucide-react"

const Command = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "flex h-10 w-full items-center rounded-md border bg-background px-3 text-sm",
      className
    )}
    {...props}
  />
))
Command.displayName = "Command"

const CommandInput = React.forwardRef(({ className, ...props }, ref) => (
  <div className="flex items-center border-b px-3 py-2">
    <Search className="mr-2 h-4 w-4 opacity-50" />
    <input
      ref={ref}
      className={cn(
        "w-full bg-transparent text-sm outline-none placeholder:text-muted-foreground",
        className
      )}
      {...props}
    />
  </div>
))
CommandInput.displayName = "CommandInput"

const CommandList = ({ children, className }) => (
  <div className={cn("max-h-60 overflow-y-auto", className)}>{children}</div>
)

const CommandItem = ({ children, className, ...props }) => (
  <button
    className={cn(
      "flex w-full cursor-pointer items-center px-3 py-2 text-sm hover:bg-accent hover:text-accent-foreground",
      className
    )}
    {...props}
  >
    {children}
  </button>
)

export { Command, CommandInput, CommandList, CommandItem }
