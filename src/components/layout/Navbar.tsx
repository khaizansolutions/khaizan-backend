'use client'
import { useState } from 'react'
import Link from 'next/link'
import { ShoppingCart, Menu, X, FileText } from 'lucide-react'
import { useQuote } from '@/context/QuoteContext'
import SmartSearch from '@/components/common/SmartSearch'

export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const { getQuoteCount } = useQuote()

  const categories = [
    { name: 'Office Supplies', href: '/products?category=office-supplies' },
    { name: 'Paper Products', href: '/products?category=paper' },
    { name: 'Ink & Toner', href: '/products?category=ink-toner' },
    { name: 'Office Machines', href: '/products?category=machines' },
    { name: 'Technology', href: '/products?category=technology' },
    { name: 'Furniture', href: '/products?category=furniture' },
  ]

  return (
    <nav className="bg-white shadow-md sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between py-4">
          <Link href="/" className="text-2xl font-bold text-primary">
            Khaizan<span className="text-secondary">Solutions</span>
          </Link>

          {/* Smart Search - Desktop */}
          <div className="hidden md:flex flex-1 max-w-xl mx-8">
            <SmartSearch />
          </div>

          <div className="flex items-center gap-4">
            <Link href="/quote" className="relative hover:text-primary">
              <FileText size={28} />
              {getQuoteCount() > 0 && (
                <span className="absolute -top-2 -right-2 bg-secondary text-white text-xs rounded-full h-5 w-5 flex items-center justify-center font-bold">
                  {getQuoteCount()}
                </span>
              )}
            </Link>
            <button 
              className="md:hidden"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? <X size={28} /> : <Menu size={28} />}
            </button>
          </div>
        </div>

        {/* Categories - Desktop */}
        <div className="hidden md:flex items-center justify-center gap-8 py-3 border-t">
          {categories.map((category) => (
            <Link
              key={category.name}
              href={category.href}
              className="text-gray-700 hover:text-primary font-medium transition"
            >
              {category.name}
            </Link>
          ))}
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 border-t">
            {/* Smart Search - Mobile */}
            <div className="mb-4">
              <SmartSearch onClose={() => setMobileMenuOpen(false)} />
            </div>
            
            {/* Mobile Categories */}
            {categories.map((category) => (
              <Link
                key={category.name}
                href={category.href}
                className="block py-2 text-gray-700 hover:text-primary hover:bg-gray-100 px-4"
                onClick={() => setMobileMenuOpen(false)}
              >
                {category.name}
              </Link>
            ))}
          </div>
        )}
      </div>
    </nav>
  )
}