'use client'
import Link from 'next/link'
import Image from 'next/image'
import { ShoppingCart, MessageCircle } from 'lucide-react'
import { useQuote } from '@/context/QuoteContext'

interface Product {
  id: number
  name: string
  price: number
  image: string
  category: string
}

interface ProductCardProps {
  product: Product
}

export default function ProductCard({ product }: ProductCardProps) {
  const { addToQuote } = useQuote()

  const handleWhatsApp = () => {
    const message = `Hi, I'm interested in:\n\n*${product.name}*\nPrice: AED ${product.price.toFixed(2)}\nCategory: ${product.category}\n\nCould you provide more details?`
    const whatsappUrl = `https://wa.me/971445222261?text=${encodeURIComponent(message)}`
    window.open(whatsappUrl, '_blank')
  }

  const handleAddToQuote = () => {
    addToQuote(product)
    alert('Added to quote list!')
  }

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden group hover:shadow-xl transition">
      <Link href={`/products/${product.id}`}>
        <div className="relative h-40 sm:h-48 md:h-56 lg:h-64 overflow-hidden bg-gray-100">
          <Image
            src={product.image}
            alt={product.name}
            fill
            className="object-cover group-hover:scale-110 transition duration-300"
          />
          <div className="absolute top-2 right-2">
            <span className="bg-secondary text-white px-2 py-1 text-[10px] sm:text-xs rounded">
              {product.category}
            </span>
          </div>
        </div>
      </Link>

      <div className="p-2 sm:p-3 md:p-4">
        <Link href={`/products/${product.id}`}>
          <h3 className="font-semibold text-gray-800 mb-2 hover:text-primary line-clamp-2 text-xs sm:text-sm md:text-base leading-tight">
            {product.name}
          </h3>
        </Link>
        <div className="text-base sm:text-lg md:text-xl lg:text-2xl font-bold text-primary mb-2 sm:mb-3 md:mb-4">
          AED {product.price.toFixed(2)}
        </div>

        {/* Desktop Buttons - Side by Side */}
        <div className="hidden md:flex gap-2">
          <button 
            onClick={handleAddToQuote}
            className="flex-1 bg-primary text-white py-2 px-3 rounded-lg hover:bg-blue-700 transition flex items-center justify-center gap-2 text-sm"
          >
            <ShoppingCart size={18} />
            Add to Quote
          </button>
          <button 
            onClick={handleWhatsApp}
            className="bg-green-500 text-white p-2 rounded-lg hover:bg-green-600 transition"
            title="Inquire on WhatsApp"
          >
            <MessageCircle size={18} />
          </button>
        </div>

        {/* Mobile Buttons - Stacked Vertically */}
        <div className="flex md:hidden flex-col gap-1.5 sm:gap-2">
          <button 
            onClick={handleAddToQuote}
            className="w-full bg-primary text-white py-1.5 sm:py-2 px-2 rounded-lg hover:bg-blue-700 transition flex items-center justify-center gap-1 sm:gap-1.5 text-[10px] sm:text-xs"
          >
            <ShoppingCart size={12} className="sm:w-4 sm:h-4" />
            <span>Add to Quote</span>
          </button>
          <button 
            onClick={handleWhatsApp}
            className="w-full bg-green-500 text-white py-1.5 sm:py-2 px-2 rounded-lg hover:bg-green-600 transition flex items-center justify-center gap-1 sm:gap-1.5 text-[10px] sm:text-xs"
          >
            <MessageCircle size={12} className="sm:w-4 sm:h-4" />
            <span>WhatsApp</span>
          </button>
        </div>
      </div>
    </div>
  )
}
