# Platforms to research 2026 06 01
* render
* railway
* vercel
* fly.io
* netlify
* github?


## Managed PaaS (Best for Speed & Simplicity)
These platforms deploy your code directly from GitHub, handle SSL certificates automatically, and manage all server infrastructure. [2, 3] 

* Render: Best overall for modern web apps. Offers a generous free tier for static sites, web services, and PostgreSQL databases. Web services spin down after inactivity on the free tier. [4, 5, 6, 7, 8] 
* Railway: Excellent developer experience. Provides a usage-based free trial ($5 one-time credit) and supports instant provisioning of databases (Postgres, MongoDB, Redis). [9, 10, 11, 12] 
* Fly.io: Best for global latency. Runs your app in micro-virtual machines close to your users. Includes a free tier that covers small applications and databases. [13, 14, 15, 16, 17] 
* Vercel: Best for frontend-heavy MVPs. Optimized for Next.js, React, and static frameworks. Features a powerful, fast global CDN and an exceptional hobbyist free tier. [18, 19, 20, 21, 22] 
* Netlify: Great for Jamstack and serverless architectures. Integrates perfectly with GitHub for instant continuous deployment. [23, 24, 25] 

## Backend-as-a-Service (Best for Mobile & Fast Backends) [26, 27] 
If you want to avoid writing standard backend code (authentication, database management, APIs), use a BaaS platform. [28, 29] 

* Supabase: The leading open-source Firebase alternative. Built on top of PostgreSQL, providing real-time data sync, user authentication, and storage with a robust free tier. [30, 31, 32, 33, 34] 
* Firebase: Google's app development platform. Ideal for real-time mobile and web apps, offering free hosting, NoSQL databases, and authentication up to generous limits. [35, 36, 37] 

## Direct Comparison

| Platform [38, 39, 40, 41, 42] | Best For | Free Tier Details | Scalability |
|---|---|---|---|
| Render | Full-stack Node/Python/Go | Free web services & Postgres | Easy slider scaling |
| Railway | Quick database + backend setup | $5 free trial credit | Automatic based on load |
| Fly.io | Low-latency global apps | 3 micro VMs + 3GB storage | Highly scalable VMs |
| Vercel | Next.js and React frontends | Free for personal/MVP use | Managed serverless edge |
| Supabase | Postgres backend & Auth | 2 free projects, 500MB DB | Seamless database upgrades |

If you are building a standard frontend+backend app, start with Render or Railway. If you are building a serverless Javascript application, choose Vercel. [43, 44, 45, 46] 
To help select the perfect fit, what programming language or framework (e.g., Python, Node.js, React) are you using? Also, does your MVP require a specific database? [47]
