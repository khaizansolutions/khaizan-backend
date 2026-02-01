'use client'
import { createContext, useContext, useState, useEffect } from 'react'

const QuoteContext = createContext()

export function QuoteProvider({ children }) {
  const [quoteItems, setQuoteItems] = useState([])

  // Load from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('quoteItems')
    if (saved) {
      setQuoteItems(JSON.parse(saved))
    }
  }, [])

  // Save to localStorage whenever items change
  useEffect(() => {
    localStorage.setItem('quoteItems', JSON.stringify(quoteItems))
  }, [quoteItems])

  const addToQuote = (product) => {
    const exists = quoteItems.find(item => item.id === product.id)
    if (exists) {
      setQuoteItems(quoteItems.map(item =>
        item.id === product.id
          ? { ...item, quantity: item.quantity + 1 }
          : item
      ))
    } else {
      setQuoteItems([...quoteItems, { ...product, quantity: 1 }])
    }
  }

  const removeFromQuote = (productId) => {
    setQuoteItems(quoteItems.filter(item => item.id !== productId))
  }

  const updateQuantity = (productId, quantity) => {
    if (quantity < 1) {
      removeFromQuote(productId)
      return
    }
    setQuoteItems(quoteItems.map(item =>
      item.id === productId ? { ...item, quantity } : item
    ))
  }

  const clearQuote = () => {
    setQuoteItems([])
  }

  const getQuoteCount = () => {
    return quoteItems.reduce((sum, item) => sum + item.quantity, 0)
  }

  return (
    <QuoteContext.Provider value={{
      quoteItems,
      addToQuote,
      removeFromQuote,
      updateQuantity,
      clearQuote,
      getQuoteCount
    }}>
      {children}
    </QuoteContext.Provider>
  )
}

export function useQuote() {
  const context = useContext(QuoteContext)
  if (!context) {
    throw new Error('useQuote must be used within QuoteProvider')
  }
  return context
}