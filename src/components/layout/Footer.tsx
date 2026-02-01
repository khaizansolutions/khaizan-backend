import Link from 'next/link'
import { Facebook, Twitter, Instagram, Linkedin } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-white mt-16">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Company Info */}
          <div>
            <h3 className="text-xl font-bold mb-4 text-secondary">OfficeSupplies</h3>
            <p className="text-gray-400 mb-4">
              Your trusted partner for all office supplies needs. Quality products at affordable prices.
            </p>
            <div className="flex gap-4">
              <a href="#" className="hover:text-secondary"><Facebook size={20} /></a>
              <a href="#" className="hover:text-secondary"><Twitter size={20} /></a>
              <a href="#" className="hover:text-secondary"><Instagram size={20} /></a>
              <a href="#" className="hover:text-secondary"><Linkedin size={20} /></a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-bold mb-4">Quick Links</h4>
            <ul className="space-y-2">
              <li><Link href="/about" className="text-gray-400 hover:text-white">About Us</Link></li>
              <li><Link href="/contact" className="text-gray-400 hover:text-white">Contact Us</Link></li>
              <li><Link href="/products" className="text-gray-400 hover:text-white">Products</Link></li>
              <li><Link href="/faq" className="text-gray-400 hover:text-white">FAQ</Link></li>
            </ul>
          </div>

          {/* Categories */}
          <div>
            <h4 className="font-bold mb-4">Categories</h4>
            <ul className="space-y-2">
              <li><Link href="/products" className="text-gray-400 hover:text-white">Office Supplies</Link></li>
              <li><Link href="/products" className="text-gray-400 hover:text-white">Paper Products</Link></li>
              <li><Link href="/products" className="text-gray-400 hover:text-white">Ink & Toner</Link></li>
              <li><Link href="/products" className="text-gray-400 hover:text-white">Technology</Link></li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="font-bold mb-4">Contact Info</h4>
            <ul className="space-y-2 text-gray-400">
              <li>123 Business Street</li>
              <li>Dubai, UAE</li>
              <li>Phone: +971 4 452 2261</li>
              <li>Email: info@officesupplies.com</li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; 2024 Office Supplies Store. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}