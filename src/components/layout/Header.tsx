'use client'
import { Phone, Mail } from 'lucide-react'
import Link from 'next/link'

export default function Header() {
  return (
    <div className="bg-primary text-white py-2 px-3 md:px-4">
      <div className="container mx-auto flex justify-between items-center text-xs md:text-sm">
        {/* Contact Info - Responsive */}
        <div className="flex items-center gap-3 md:gap-6">
          <a 
            href="tel:+97144522261" 
            className="flex items-center gap-1 md:gap-2 hover:text-secondary transition"
          >
            <Phone size={14} className="md:w-4 md:h-4" />
            <span className="hidden sm:inline">+971 4 452 2261</span>
            <span className="sm:hidden">Call Us</span>
          </a>
          <a 
            href="mailto:info@khaizensolutions.com" 
            className="flex items-center gap-1 md:gap-2 hover:text-secondary transition"
          >
            <Mail size={14} className="md:w-4 md:h-4" />
            <span className="hidden md:inline">info@khaizensolutions.com</span>
            <span className="md:hidden hidden sm:inline">Email</span>
          </a>
        </div>

        {/* Sign In / Register - Mobile Optimized */}
        <div className="flex items-center gap-2 md:gap-4">
          <Link 
            href="/login" 
            className="hover:text-secondary transition px-2 py-1"
          >
            Sign In
          </Link>
          <span className="text-gray-300">|</span>
          <Link 
            href="/register" 
            className="hover:text-secondary transition px-2 py-1"
          >
            Register
          </Link>
        </div>
      </div>
    </div>
  )
}