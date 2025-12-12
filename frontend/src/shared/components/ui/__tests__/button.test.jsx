import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from '../button'

describe('Button Component', () => {
  it('renders button with text', () => {
    render(<Button>Click me</Button>)
    const button = screen.getByRole('button')
    expect(button).toBeInTheDocument()
    expect(button).toHaveTextContent('Click me')
  })

  it('handles click events', () => {
    const handleClick = vi.fn()
    render(<Button onClick={handleClick}>Click me</Button>)
    
    const button = screen.getByRole('button')
    fireEvent.click(button)
    
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('applies variant classes correctly', () => {
    const { rerender } = render(<Button variant="default">Default</Button>)
    let button = screen.getByRole('button')
    expect(button.className).toContain('bg-primary')

    rerender(<Button variant="outline">Outline</Button>)
    button = screen.getByRole('button')
    expect(button.className).toContain('border')
  })

  it('can be disabled', () => {
    render(<Button disabled>Disabled</Button>)
    const button = screen.getByRole('button')
    expect(button).toBeDisabled()
  })

  it('supports different sizes', () => {
    const { rerender } = render(<Button size="default">Default</Button>)
    let button = screen.getByRole('button')
    expect(button.className).toContain('h-10')

    rerender(<Button size="sm">Small</Button>)
    button = screen.getByRole('button')
    expect(button.className).toContain('h-9')

    rerender(<Button size="lg">Large</Button>)
    button = screen.getByRole('button')
    expect(button.className).toContain('h-11')
  })
})
