In modern atomic theory, electrons don’t follow neat little circular tracks like planets around the Sun. Instead, quantum mechanics tells us that an electron bound to a nucleus occupies a “cloud” of probability. Nevertheless, it’s still useful to talk about a characteristic or average distance from the nucleus. Below are two complementary ways to think about that distance:

1. The Bohr Model (Historical, Semi-Classical)  
   • Bohr postulated that electrons move in fixed circular orbits around the nucleus with quantized radii.  
   • The radius of the nth orbit in a hydrogen-like atom is  
     rₙ = (ε₀·h²)/(π·m_e·e²) · n²  
     where  
       • ε₀ is the vacuum permittivity  
       • h is Planck’s constant  
       • m_e is the electron mass  
       • e is the elementary charge  
       • n = 1, 2, 3, … is the principal quantum number  
   • For hydrogen (n = 1), this gives the famous Bohr radius  
     a₀ ≃ 0.529 Å (0.529 × 10⁻¹⁰ m).  
   • Higher n → orbits whose radii grow like n².

2. Quantum-Mechanical Orbitals (Probability Clouds)  
   • In Schrödinger’s wave-mechanical model, each electron is described by a wavefunction ψ(r, θ, ϕ).  
   • The probability of finding the electron at a distance between r and r + dr is  
       P(r) dr = |ψ(r, θ, ϕ)|² · 4πr² dr  (after integrating over angles).  
   • For the hydrogen 1s orbital, ψ₁s ∝ e^(–r/a₀), so  
       P₁s(r) = 4 r² a₀⁻³ e^(–2r/a₀) dr.  
     This has its maximum at r = a₀, meaning you’re most likely to find the electron about one Bohr radius from the nucleus—but there’s a finite probability both inside and outside that radius.  
   • For excited states (n > 1) and orbitals with angular momentum (p, d, f…), the radial probability distribution has multiple peaks and nodes, but its overall scale still involves the factor n²·a₀.

Key Takeaways  
• The “orbital distance” is not a sharp boundary but a most-probable or average radius derived from the electron’s wavefunction.  
• In the simplest hydrogenic case, that distance scales as n²·a₀.  
• Real multi-electron atoms introduce screening and more complex wavefunctions, but the Bohr radius remains the fundamental unit for estimating atomic size.