# service-detail.py

html_template = """
{{% extends "myapp/base.html" %}}

{{% block title %}}Service Details{{% endblock %}}

{{% load static %}}
{{% block content %}}

<body>

<div class="page-wrapper">
	
	<!-- Cursor -->
	<div class="cursor"></div>
	<div class="cursor-follower"></div>
	<!-- Cursor End -->
 	
	<!-- Preloader -->
	  <!--       
	<div class="loader-wrap">
		<div class="preloader">
			<div class="preloader-close">x</div>
			<div id="handle-preloader" class="handle-preloader">
				<div class="animation-preloader">
					<div class="txt-loading">
						<span data-text-preloader="L" class="letters-loading">L</span>
						<span data-text-preloader="O" class="letters-loading">O</span>
						<span data-text-preloader="A" class="letters-loading">A</span>
						<span data-text-preloader="D" class="letters-loading">D</span>
						<span data-text-preloader="I" class="letters-loading">I</span>
						<span data-text-preloader="N" class="letters-loading">N</span>
						<span data-text-preloader="G" class="letters-loading">G</span>
					</div>
				</div>
			</div>
		</div>
	</div>
	-->
	<!-- Preloader End -->
	
	<!-- Main Header -->
{{% include 'header.html' %}}
	<!-- End Main Header -->
	
	<!-- Page Title -->
    <section class="page-title">
		<div class="page-title-icon"></div>
			<div class="page-title-icon-two"></div>
			<div class="page-title-shadow"></div>
			<div class="page-title-shadow-two"></div>
        <div class="auto-container">
			<h2>Service details</h2>
			<ul class="bread-crumb clearfix">
				<li><a href="{{% url 'index' %}}">Home</a></li>
				<li>Service details</li>
			</ul>
        </div>
    </section>
    <!-- End Page Title -->

	<!-- Services Detail -->
	<section class="services-detail">
		<div class="auto-container">
			<!-- Sec Title -->
			<div class="sec-title style-four">
				<div class="d-flex justify-content-between align-items-center flex-wrap">
					<div class="left-box">
						<div class="sec-title_title">content marketers</div>
						<h2 class="sec-title_heading">Navigating the digital landscape with <span>content marketing</span></h2>
					</div>
					<div class="right-box">
						<p>Lorem ipsum dolor sit amet consectetur adipiscing elit Ut et massa  Aliquam in hendrerit urna. Pellentesque sit amet sapien fringilla, mattis l consectetur, ultrices mauris. Maecenas vitae mattis tellus. Nullam quis imperdiet augue. Vestibulum auctor ornare leo, non suscipit magna</p>
						<p>Lorem ipsum dolor sit amet consectetur adipiscing elit Ut et massa  Aliquam in hendrerit urna pellentesque</p>
					</div>
				</div>
			</div>
			<div class="service-detail_image">
				<img src="{{% static 'myapp/images/resource/service-detail.jpg' %}}" alt="" />
			</div>
		</div>
	</section>
	<!-- End Services One -->

	<!-- Services Two -->
	<div class="services-two">
		<div class="auto-container">
			<!-- Sec Title -->
			<div class="sec-title style-four centered">
				<div class="sec-title_title">Service benefit</div>
				<h2 class="sec-title_heading"><span>Benefit</span> of our services</h2>
			</div>
			<div class="row clearfix">

				<!-- Service Block Four -->
				<div class="service-block_four col-lg-3 col-md-6 col-sm-12">
					<div class="service-block_four-inner">
						<div class="service-block_four-icon">
							<i class="icon-heart-hand"></i>
						</div>
						<h4 class="service-block_four-title">Engagement</h4>
						<div class="service-block_four-text">Design patent protects the unique visual aspects of your product, preventing.</div>
					</div>
				</div>

				<!-- Service Block Four -->
				<div class="service-block_four col-lg-3 col-md-6 col-sm-12">
					<div class="service-block_four-inner">
						<div class="service-block_four-icon">
							<i class="icon-eye"></i>
						</div>
						<h4 class="service-block_four-title">Brand visibility</h4>
						<div class="service-block_four-text">Design patent protects the unique visual aspects of your product, preventing.</div>
					</div>
				</div>

				<!-- Service Block Four -->
				<div class="service-block_four col-lg-3 col-md-6 col-sm-12">
					<div class="service-block_four-inner">
						<div class="service-block_four-icon">
							<i class="icon-seo"></i>
						</div>
						<h4 class="service-block_four-title">SEO optimization</h4>
						<div class="service-block_four-text">Design patent protects the unique visual aspects of your product, preventing.</div>
					</div>
				</div>

				<!-- Service Block Four -->
				<div class="service-block_four col-lg-3 col-md-6 col-sm-12">
					<div class="service-block_four-inner">
						<div class="service-block_four-icon">
							<i class="icon-magnet-1"></i>
						</div>
						<h4 class="service-block_four-title">Lead generation</h4>
						<div class="service-block_four-text">Design patent protects the unique visual aspects of your product, preventing.</div>
					</div>
				</div>

			</div>
		</div>
	</div>
	<!-- End Services Two -->

	<!-- Steps One -->
	<section class="steps-one">
		<div class="steps-one_bg"></div>
		<div class="steps-one_icon"></div>

		<div class="auto-container">
			<div class="inner-container">
				<div class="circle-layer"></div>
				<div class="dots-layer">
					<span class="dot-one"></span>
					<span class="dot-two"></span>
				</div>
			
				<!-- Sec Title -->
				<div class="sec-title">
					<div class="sec-title_title">How Its work</div>
					<h2 class="sec-title_heading">iRiseUp Academy <span>typically operate</span> in <br> a three steps</h2>
				</div>
				<div class="steps-one_button">
					<a href="{{% url 'about' %}}" class="template-btn btn-style-two">
						<span class="btn-wrap">
							<span class="text-one">Know more</span>
							<span class="text-two">Know more</span>
						</span>
					</a>
				</div>
				<div class="row clearfix">
					<!-- Column -->
					<div class="column col-lg-6 col-md-12 col-sm-12">
						<!-- Step Block One -->
						<div class="step-block_one">
							<div class="step-block_one-inner">
								<div class="step-block_one-steps">step 01</div>
								<h5 class="step-block_one-title">Algorithm processing</h5>
								<div class="step-block_one-text">Lorem ipsum dolor sit ame consectetur adipiscing elit Ut et massa mi. Aliquam in hendrerit urna..</div>
								<div class="step-block_one-content">
									<div class="image">
										<img src="{{% static 'myapp/images/resource/step-1.png' %}}" alt="" />
									</div>
								</div>
							</div>
						</div>
					</div>
					<!-- Column -->
					<div class="column col-lg-6 col-md-12 col-sm-12">

						<!-- Step Block One -->
						<div class="step-block_one">
							<div class="step-block_one-inner">
								<div class="step-block_one-steps">step 02</div>
								<h5 class="step-block_one-title">Input & data gathering</h5>
								<div class="step-block_one-text">Lorem ipsum dolor sit ame consectetur adipiscing elit Ut et massa mi. Aliquam in hendrerit urna..</div>
								<div class="step-block_one-content">
									<div class="image">
										<img src="{{% static 'myapp/images/resource/step-2.png' %}}" alt="" />
									</div>
								</div>
							</div>
						</div>

						<!-- Step Block One -->
						<div class="step-block_one">
							<div class="step-block_one-inner">
								<div class="step-block_one-steps">step 03</div>
								<h5 class="step-block_one-title">Content generation & refinement</h5>
								<div class="step-block_one-text">Lorem ipsum dolor sit ame consectetur adipiscing elit Ut et massa mi. Aliquam in hendrerit urna..</div>
								<div class="step-block_one-content">
									<div class="image">
										<img src="{{% static 'myapp/images/resource/step-3.png' %}}" alt="" />
									</div>
								</div>
							</div>
						</div>

					</div>
				</div>
			</div>
		</div>
	</section>
	<!-- End Steps One -->

	<!-- Solution One -->
	<section class="solution-one">
		<div class="auto-container">
			<!-- Sec Title -->
			<div class="sec-title style-four">
				<div class="d-flex justify-content-between align-items-center flex-wrap">
					<div class="left-box">
						<div class="sec-title_title">problem & solutions</div>
						<h2 class="sec-title_heading">Unveiling <span>solutions</span> for common dilemmas in iRiseUp Academy</h2>
					</div>
					<div class="right-box">
						<p>Lorem ipsum dolor sit amet consectetur adipiscing elit Ut et massa  Aliquam in hendrerit urna. Pellentesque sit amet sapien fringilla, mattis l consectetur, ultrices mauris. Maecenas vitae mattis tellus. Nullam quis imperdiet augue. Vestibulum auctor ornare leo, non suscipit magna</p>
						<ul class="solution-one_list">
							<li><i class="fa-solid fa-check fa-fw"></i>Sed tempor magna et risus ornare, a lobortis.</li>
							<li><i class="fa-solid fa-check fa-fw"></i>Vivamus tempus urna sit amet ante imperdiet.</li>
							<li><i class="fa-solid fa-check fa-fw"></i>Mauris sit amet eros ac tellus egestas placerat.</li>
							<li><i class="fa-solid fa-check fa-fw"></i>Aliquam at leo pretium of consecteter.</li>
						</ul>
					</div>
				</div>
			</div>
			<div class="row clearfix">
				<div class="column col-lg-6 col-md-6 col-sm-12">
					<div class="service-detail_image-two">
						<img src="{{% static 'myapp/images/resource/service-detail-1.jpg' %}}" alt="" />
					</div>
				</div>
				<div class="column col-lg-6 col-md-6 col-sm-12">
					<div class="service-detail_image-two">
						<a href="https://www.youtube.com/watch?v=kxPCFljwJws" class="lightbox-video service-detail_play"><span class="fa-solid fa-play fa-fw"><i class="ripple"></i></span></a>
						<img src="{{% static 'myapp/images/resource/service-detail-2' %}}" alt="" />
					</div>
				</div>
			</div>

			<!-- Sec Title -->
			<div class="sec-title style-four">
				<div class="d-flex justify-content-between align-items-center flex-wrap">
					<div class="left-box">
						<div class="sec-title_title">Final result</div>
						<h2 class="sec-title_heading">Excellence in our service <span>final results</span></h2>
					</div>
					<div class="right-box">
						<p>Lorem ipsum dolor sit amet consectetur adipiscing elit Ut et massa  Aliquam in hendrerit urna. Pellentesque sit amet sapien fringilla, mattis l consectetur, ultrices mauris. Maecenas vitae mattis tellus.</p>
						<p>Pellentesque commodo lacus at sodales sodales. Quisque lorem sagittis orci ut diam condimentum, vel euismod</p>
					</div>
				</div>
			</div>
		</div>
	</section>
	<!-- End Solution One -->

	<!-- Faq One -->
	<section class="faq-one style-three">
		<div class="auto-container">
			<div class="row clearfix">

				<!-- Tab Column -->
				<div class="faq-one_title-column col-lg-5 col-md-12 col-sm-12">
					<div class="faq-one_title-outer">
						<!-- Sec Title -->
						<div class="sec-title">
							<div class="sec-title_title">faq</div>
							<h2 class="sec-title_heading">Frequently asked <span>questions</span></h2>
							<div class="sec-title_text">Lorem ipsum dolor sit amet consectetur adipiscing vitae mattis tellus. Nullam quis mattis ligula consectetur.</div>
						</div>
						<div class="faq-one_button">
							<a href="{{% url 'contact' %}}" class="template-btn btn-style-one">
								<span class="btn-wrap">
									<span class="text-one">Contact now</span>
									<span class="text-two">Contact now</span>
								</span>
							</a>
						</div>
					</div>
				</div>

				<!-- Accordian Column -->
				<div class="faq-one_accordian-column col-lg-7 col-md-12 col-sm-12">
					<div class="faq-one_accordian-outer">

						<!-- Accordion Box -->
						<ul class="accordion-box_two">
									
							<!-- Block -->
							<li class="accordion block">
								<div class="acc-btn"><div class="icon-outer"><span class="icon icon-plus fa-solid fa-plus fa-fw"></span></div>How does your AI copywriting tool work?</div>
								<div class="acc-content">
									<div class="content">
										<div class="text">Our AI copywriting tool uses sophisticated algorithms to understand context, tone, and language nuances. Users input specific details or prompts, and the AI generates high-quality content based on that input, refining.</div>
									</div>
								</div>
							</li>
										
							<!-- Block -->
							<li class="accordion block">
								<div class="acc-btn"><div class="icon-outer"><span class="icon icon-plus fa-solid fa-plus fa-fw"></span></div>What is AI copywriting?</div>
								<div class="acc-content">
									<div class="content">
										<div class="text">Our AI copywriting tool uses sophisticated algorithms to understand context, tone, and language nuances. Users input specific details or prompts, and the AI generates high-quality content based on that input, refining.</div>
									</div>
								</div>
							</li>

							<!-- Block -->
							<li class="accordion block">
								<div class="acc-btn"><div class="icon-outer"><span class="icon icon-plus fa-solid fa-plus fa-fw"></span></div>Can I trust the content generated by AI?</div>
								<div class="acc-content">
									<div class="content">
										<div class="text">Our AI copywriting tool uses sophisticated algorithms to understand context, tone, and language nuances. Users input specific details or prompts, and the AI generates high-quality content based on that input, refining.</div>
									</div>
								</div>
							</li>

							<!-- Block -->
							<li class="accordion block">
								<div class="acc-btn"><div class="icon-outer"><span class="icon icon-plus fa-solid fa-plus fa-fw"></span></div>What types of content can your AI generate?</div>
								<div class="acc-content">
									<div class="content">
										<div class="text">Our AI copywriting tool uses sophisticated algorithms to understand context, tone, and language nuances. Users input specific details or prompts, and the AI generates high-quality content based on that input, refining.</div>
									</div>
								</div>
							</li>

							<!-- Block -->
							<li class="accordion block">
								<div class="acc-btn"><div class="icon-outer"><span class="icon icon-plus fa-solid fa-plus fa-fw"></span></div>What languages does your AI support?</div>
								<div class="acc-content">
									<div class="content">
										<div class="text">Our AI copywriting tool uses sophisticated algorithms to understand context, tone, and language nuances. Users input specific details or prompts, and the AI generates high-quality content based on that input, refining.</div>
									</div>
								</div>
							</li>

						</ul>

					</div>
				</div>

			</div>
		</div>
	</section>
	<!-- End Faq One -->

	<div class="more-options">
		<div class="auto-container">
			<!-- Post Share Options-->
			<div class="post-share-options">
				<div class="post-share-inner d-flex justify-content-between align-items-center flex-wrap">
					<div class="post-tags"><a href="#">DataAI</a> <a href="#">AIFuture</a> <a href="#">AIExperts</a></div>
					<ul class="social-links">
						<li><a href="#" class="fa-brands fa-facebook-f fa-fw"></a></li>
						<li><a href="#" class="fa-brands fa-twitter fa-fw"></a></li>
						<li><a href="#" class="fa-brands fa-google fa-fw"></a></li>
						<li><a href="#" class="fa-brands fa-dribbble fa-fw"></a></li>
					</ul>
				</div>
			</div>

			<div class="service-detail_posts">
				<div class="d-flex align-items-center flex-wrap justify-content-between">
					<div class="new-post">
						<a href="#"><i class="fa-solid fa-angle-left fa-fw"></i> Previous</a>
						<h4>Protection of designs</h4>
					</div>
					<div class="new-post text-right">
						<a href="#">next <i class="fa-solid fa-angle-right fa-fw"></i></a>
						<h4>Brand protection</h4>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- CTA One -->
	{{% include 'ctaone.html' %}}
	<!-- End CTA One -->

	<!-- Main Footer -->
	{{% include 'footer.html' %}}
<!-- End PageWrapper -->
{{% endblock %}}
"""

for i in range(1, 5):
    file_content = html_template.format(i)
    file_name = f"service-detail-{i}.html"
    with open(file_name, "w") as file:
        file.write(file_content)

print("HTML files created successfully.")
