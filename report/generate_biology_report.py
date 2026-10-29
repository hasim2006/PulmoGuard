import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

from generate_report_helpers import (
    set_cell_background,
    set_cell_margins,
    set_table_borders,
    add_callout,
    add_heading_1,
    add_heading_2,
    add_heading_3,
    add_body_p,
    add_bullet_p,
    add_figure_with_caption
)

def create_report():
    doc = docx.Document()
    
    # 1. Page Margins Setup (1 inch all around)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Header Setup
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("BIOLOGY EXPERIENTIAL LEARNING REPORT | Cell Press Deep Learning Study")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(120, 130, 145)
        
        # Footer Setup with Page Numbering
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        frun1 = fp.add_run("Page ")
        frun1.font.name = "Calibri"
        frun1.font.size = Pt(8.5)
        frun1.font.color.rgb = RGBColor(120, 130, 145)
        
        fldSimple = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
        fp._p.append(fldSimple)
        
        frun2 = fp.add_run(" of ")
        frun2.font.name = "Calibri"
        frun2.font.size = Pt(8.5)
        frun2.font.color.rgb = RGBColor(120, 130, 145)
        
        fldSimple2 = parse_xml(r'<w:fldSimple %s w:instr="NUMPAGES"/>' % nsdecls('w'))
        fp._p.append(fldSimple2)

    # -------------------------------------------------------------
    # DOCUMENT COVER / TITLE HEADER BLOCK
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(12)
    title_p.paragraph_format.space_after = Pt(4)
    run_super = title_p.add_run("BIOLOGY EXPERIENTIAL LEARNING REPORT\n")
    run_super.font.name = "Calibri"
    run_super.font.size = Pt(13)
    run_super.font.bold = True
    run_super.font.color.rgb = RGBColor(0x2C, 0x5E, 0x8A)
    
    run_title = title_p.add_run("Identifying Medical Diagnoses and Treatable Diseases by Image-Based Deep Learning")
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    
    subtitle_p = doc.add_paragraph()
    subtitle_p.paragraph_format.space_before = Pt(2)
    subtitle_p.paragraph_format.space_after = Pt(14)
    run_sub = subtitle_p.add_run("A Transfer Learning Diagnostic Framework for Retinal Optical Coherence Tomography and Pediatric Chest Radiography")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(12)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(0x55, 0x66, 0x77)
    
    # Metadata Block Table
    meta_tbl = doc.add_table(rows=4, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_tbl.autofit = False
    set_table_borders(meta_tbl, color="D3D9E2", sz="4", val="single")
    
    col_widths = [Inches(1.8), Inches(4.7)]
    meta_data = [
        ("Source Publication:", "Cell (Volume 172, Issue 5, pp. 1122–1131.e9, February 22, 2018)"),
        ("Original Paper DOI:", "https://doi.org/10.1016/j.cell.2018.02.010 | Cell Press Archive"),
        ("Lead & Senior Authors:", "Daniel S. Kermany, Michael Goldbaum, Wenjia Cai, Carolina C.S. Valentim, Kang Zhang et al."),
        ("Academic Disciplines:", "Translational Biology, Computational Medicine, Ophthalmology, Pulmonology, Transfer Learning")
    ]
    for row_idx, (k, v) in enumerate(meta_data):
        row = meta_tbl.rows[row_idx]
        cell_k, cell_v = row.cells[0], row.cells[1]
        cell_k.width, cell_v.width = col_widths[0], col_widths[1]
        set_cell_background(cell_k, "F0F4F8")
        set_cell_background(cell_v, "FFFFFF")
        set_cell_margins(cell_k, top=60, bottom=60, left=100, right=80)
        set_cell_margins(cell_v, top=60, bottom=60, left=100, right=80)
        
        pk = cell_k.paragraphs[0]
        pk.paragraph_format.line_spacing = 1.05
        pk.paragraph_format.space_after = Pt(0)
        rk = pk.add_run(k)
        rk.font.name = "Calibri"
        rk.font.size = Pt(9.5)
        rk.font.bold = True
        rk.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        
        pv = cell_v.paragraphs[0]
        pv.paragraph_format.line_spacing = 1.05
        pv.paragraph_format.space_after = Pt(0)
        rv = pv.add_run(v)
        rv.font.name = "Calibri"
        rv.font.size = Pt(9.5)
        rv.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    sp_after_meta = doc.add_paragraph()
    sp_after_meta.paragraph_format.space_after = Pt(10)

    # Graphical Abstract Callout Box & Figure
    add_callout(
        doc,
        [
            "REPORT HIGHLIGHT & GRAPHICAL ABSTRACT SUMMARY:",
            "• An image-based deep-learning diagnostic framework was constructed using transfer learning to address severe data limitations common in biomedical imaging.",
            "• Demonstrates high diagnostic performance in classifying age-related macular degeneration (AMD) and diabetic macular edema (DME) on optical coherence tomography (OCT) images.",
            "• Implements automated clinical referral triaging: accurately separating urgent referrals requiring prompt anti-VEGF injection from routine referrals (drusen) and routine observation.",
            "• Algorithmic performance matched or exceeded that of six independent human ophthalmology specialists.",
            "• Occlusion sensitivity mapping successfully verified that neural network decisions rely directly on anatomical pathological lesions (fluid pockets, neovascular membranes, and drusen).",
            "• Validates generalized cross-disciplinary utility by accurately identifying pneumonia and differentiating bacterial from viral pneumonia on pediatric chest X-rays."
        ],
        border_color="1B365D",
        fill_color="F4F7FA"
    )

    add_figure_with_caption(
        doc,
        "extracted_figures/p1_img0_Im1.jpg",
        "Graphical Abstract:",
        "Overview of the deep-learning referral and diagnostic framework. Pre-trained representations from ImageNet are transferred to ophthalmological OCT B-scans and pediatric chest radiographs, enabling clinical triaging between urgent anti-VEGF intervention (CNV, DME), routine referral (Drusen), and routine observation (Normal), as well as rapid respiratory infection triage.",
        width_inches=5.2
    )

    # -------------------------------------------------------------
    # 1. INTRODUCTION
    # -------------------------------------------------------------
    add_heading_1(doc, "1. INTRODUCTION")
    
    add_heading_2(doc, "1.1 Clinical Background & Biological Pathophysiology")
    add_body_p(
        doc,
        "Biomedical imaging plays a paramount role in modern clinical medicine, providing non-invasive, micrometer-level structural visualizations of living tissues. However, the interpretation of complex biological images currently demands highly specialized medical expertise. A critical bottleneck in global healthcare is the severe disparity between the immense volume of diagnostic imaging procedures conducted annually and the limited global workforce of board-certified medical specialists. This deficit is acutely felt in ophthalmology and pulmonary medicine, where delayed diagnosis frequently leads to irreversible tissue destruction, permanent disability, or patient mortality.",
        bold_prefix="The Clinical Imaging Dilemma: "
    )
    add_body_p(
        doc,
        "Among sensory impairments, visual disability represents one of the most debilitating conditions worldwide. Two major retinal diseases account for the predominant burden of irreversible severe central vision loss in developed and developing countries:",
        bold_prefix="Pathophysiology of Vision-Threatening Retinal Pathologies: "
    )
    add_bullet_p(
        doc,
        "A severe complication of neovascular ('wet') age-related macular degeneration (AMD). Pathologically, it is characterized by abnormal angiogenic capillary sprouting from the choroidal vasculature through defects in Bruch's membrane into the subretinal space or sub-retinal pigment epithelium (sub-RPE). Pathophysiologically driven by the overexpression of vascular endothelial growth factor (VEGF), these immature, fragile vessels readily leak plasma proteins, lipid exudates, and erythrocytes. This fluid accumulation causes neurosensory retinal detachment, photoreceptor apoptosis, and rapid formation of permanent disciform fibrovascular scars that obliterate central visual acuity if not treated promptly.",
        bold_prefix="Choroidal Neovascularization (CNV): "
    )
    add_bullet_p(
        doc,
        "The primary cause of moderate-to-severe visual impairment in the working-age diabetic population. Chronic hyperglycemia incites endothelial dysfunction, pericyte apoptosis, microaneurysm formation, and severe breakdown of the inner and outer blood-retinal barriers (BRB). Subsequent fluid extravasation into the macula produces intraretinal cystoid spaces, diffuse neuroretinal thickening, and severe disruption of synaptic transmission between photoreceptors, bipolar cells, and retinal ganglion cells.",
        bold_prefix="Diabetic Macular Edema (DME): "
    )
    add_bullet_p(
        doc,
        "The diagnostic hallmark of early-to-intermediate non-neovascular ('dry') AMD. Drusen are extracellular, nodular deposits of lipids, proteins, and cellular debris that accumulate between the basal lamina of the retinal pigment epithelium and the inner collagenous zone of Bruch's membrane. While small hard drusen may not immediately compromise visual function, confluent soft drusen confer a high prognostic risk for progression into exudative CNV or geographic atrophy.",
        bold_prefix="Drusen (Dry AMD): "
    )
    add_bullet_p(
        doc,
        "Demonstrates an intact, stratified ten-layer neurosensory cytoarchitecture, preserved foveal depression (foveal avascular zone), a continuous monolayer of RPE cells, and completely fluid-free intraretinal and subretinal tissue planes.",
        bold_prefix="Normal Retinal Architecture: "
    )
    add_body_p(
        doc,
        "Critically, CNV and DME are pharmacologically treatable if detected early. The clinical introduction of intravitreal anti-VEGF monoclonal antibodies and fusion proteins (such as ranibizumab, bevacizumab, and aflibercept) has revolutionized retinal therapy, halting angiogenic leakage and reversing macular edema. However, treatment efficacy exhibits a narrow therapeutic window: once photoreceptor death or dense subretinal fibrosis ensues, visual loss is irreversible. Consequently, triaging patients into 'urgent referrals' (requiring ophthalmological intervention within 48–72 hours) versus 'routine referrals' (drusen requiring routine monitoring) versus 'observation' (normal retina) is a life-changing clinical imperative.",
        bold_prefix="The Window of Treatability & Urgent Triage: "
    )

    add_heading_2(doc, "1.2 Biomedical Imaging Modalities: OCT and Chest Radiography")
    add_body_p(
        doc,
        "Optical Coherence Tomography (OCT) is an optical imaging modality based on low-coherence interferometry that captures cross-sectional, micrometer-resolution (~3–5 µm) cross-sections (B-scans) of the retina in vivo. Similar to an optical biopsy, OCT enables direct visualization of cellular and sub-cellular retinal stratification, including fluid-filled cystoid spaces, hyperreflective neovascular membranes, and sub-RPE drusenoid elevations. With over 30 million OCT examinations performed globally each year, the manual review of dozens of B-scans per volume creates an overwhelming clinical workload.",
        bold_prefix="Optical Coherence Tomography (OCT): "
    )
    add_body_p(
        doc,
        "To rigorously assess whether an automated image interpretation system can generalize across completely disparate anatomical systems and imaging physics, the investigation extended to pediatric chest radiography (X-rays). Childhood pneumonia remains the leading single infectious cause of mortality among children under five years of age worldwide, claiming approximately one million lives annually. In pediatric emergency care, rapid chest radiography is the frontline diagnostic tool. However, interpreting pediatric chest X-rays is fraught with diagnostic challenges: differentiating normal pediatric lung fields from infectious opacities, and more crucially, distinguishing bacterial pneumonia (characterized by focal lobar consolidations) from viral pneumonia (characterized by diffuse, bilateral interstitial infiltrates). Accurate etiological discrimination is paramount to enforcing antibiotic stewardship—ensuring prompt antibiotic therapy for bacterial cases while preventing antibiotic overuse in viral infections.",
        bold_prefix="Pediatric Chest Radiography (X-Ray): "
    )

    add_heading_2(doc, "1.3 Deep Learning & The Transfer Learning Revolution in Biology")
    add_body_p(
        doc,
        "Traditional computer vision algorithms in biomedical engineering relied heavily on handcrafted feature extraction—such as matched Gabor filters, edge detection kernels, and thresholding operators. These engineered heuristics are fragile, failing to accommodate biological variability, image artifacts, and pathological heterogeneity. Convolutional Neural Networks (CNNs) overcame these barriers by learning hierarchical spatial feature representations directly from raw pixel arrays through backpropagation.",
        bold_prefix="Limitations of Traditional Computer Vision: "
    )
    add_body_p(
        doc,
        "However, training deep neural networks from random weight initialization ('from scratch') typically requires millions of precisely annotated examples to avoid severe overfitting. In biological and medical disciplines, acquiring millions of expert-curated images is economically and logistically prohibitive. This profound challenge is resolved through Transfer Learning: leveraging knowledge gained from training on a massive, general image benchmark (such as ImageNet, comprising 1.28 million natural images categorized into 1,000 everyday object classes) and transferring that learned structural knowledge to specialized medical datasets. Lower convolutional layers in deep networks learn universal visual primitives—such as spatial gradients, edges, lines, curves, and textural patterns—which are invariant across natural scenes and biological tissues. By freezing these foundational feature extraction layers and fine-tuning only the terminal classification layers, deep models can be trained on substantially smaller clinical cohorts while achieving superior diagnostic accuracy.",
        bold_prefix="The Transfer Learning Paradigm: "
    )

    # Figure 1: Transfer Learning Architecture
    add_figure_with_caption(
        doc,
        "extracted_figures/p3_img0_Im2.jpg",
        "Figure 1: Transfer Learning and Convolutional Neural Network Workflow.",
        "Schematic representation illustrating how a deep convolutional neural network (Inception-V3) pre-trained on 1.28 million natural images from the ImageNet benchmark is adapted for specialized medical diagnosis. The universal visual feature detectors in the initial convolutional layers are frozen to prevent overfitting, while the terminal fully connected and softmax classification heads are retrained on retinal OCT and chest radiographic datasets.",
        width_inches=5.5
    )

    # -------------------------------------------------------------
    # 2. OBJECTIVES
    # -------------------------------------------------------------
    add_heading_1(doc, "2. OBJECTIVES")
    add_body_p(
        doc,
        "The overarching aim of this experimental research was to develop, validate, and clinically benchmark a generalized, transfer-learning-based artificial intelligence framework capable of automated image interpretation, diagnostic triage, and decision-making across distinct clinical domains.",
        bold_prefix="Primary Research Aim: "
    )
    add_body_p(doc, "The specific biological, computational, and clinical objectives of the investigation were formulated as follows:")
    
    add_bullet_p(
        doc,
        "Train and optimize a deep convolutional neural network (Inception-V3 architecture) on a multi-center repository of retinal optical coherence tomography (OCT) B-scans to classify images into four clinical categories: Choroidal Neovascularization (CNV), Diabetic Macular Edema (DME), Drusen, and Normal retina.",
        bold_prefix="Objective 1 (Multi-Class Retinal Diagnostic Classification): "
    )
    add_bullet_p(
        doc,
        "Construct an automated, clinically actionable decision-support triaging system that stratifies patients based on medical urgency: designating CNV and DME as 'Urgent Referrals' (requiring immediate intravitreal anti-VEGF injection within days to prevent permanent blindness), Drusen as 'Routine Referrals' (requiring non-urgent outpatient evaluation), and Normal scans for 'Routine Observation'.",
        bold_prefix="Objective 2 (Clinical Referral Triaging System): "
    )
    add_bullet_p(
        doc,
        "Directly compare the diagnostic accuracy, sensitivity, specificity, and receiver operating characteristic (ROC) curves of the AI system against six board-certified human ophthalmologists (three senior fellowship-trained vitreoretinal specialists and three general ophthalmologists) using an identical, independent test cohort.",
        bold_prefix="Objective 3 (Clinical Benchmarking Against Human Experts): "
    )
    add_bullet_p(
        doc,
        "Establish a clinically weighted error scoring methodology that explicitly penalizes high-risk diagnostic errors (e.g., misclassifying an urgent treatable CNV or DME patient as normal) far more severely than low-risk false alarms, aligning algorithmic evaluation with medical malpractice and patient safety principles.",
        bold_prefix="Objective 4 (Clinical Weighted Error Evaluation): "
    )
    add_bullet_p(
        doc,
        "Evaluate the cross-disciplinary generalizability of the transfer-learning framework by applying it to an entirely unrelated clinical problem: classifying pediatric chest radiographs into pneumonia versus normal lung parenchyma, and differentiating bacterial from viral pneumonia to guide antibiotic stewardship.",
        bold_prefix="Objective 5 (Cross-Domain Generalization to Pulmonary Medicine): "
    )
    add_bullet_p(
        doc,
        "Interrogate the 'black box' of the deep convolutional network using occlusion sensitivity mapping to biologically validate that algorithmic decision-making relies upon genuine anatomical lesions (fluid pockets, membranes, consolidations) rather than spurious background artifacts.",
        bold_prefix="Objective 6 (Explainability & Anatomical Lesion Verification): "
    )
    add_bullet_p(
        doc,
        "Assess whether the deep learning model can track longitudinal therapeutic response in retinal patients undergoing anti-VEGF therapy over successive clinical visits, confirming algorithmic utility for monitoring treatment progress.",
        bold_prefix="Objective 7 (Longitudinal Therapeutic Monitoring): "
    )

    # -------------------------------------------------------------
    # 3. RESEARCH METHODOLOGY
    # -------------------------------------------------------------
    add_heading_1(doc, "3. RESEARCH METHODOLOGY")
    
    add_heading_2(doc, "3.1 Clinical Setting, Patient Cohorts & Ethical Governance")
    add_body_p(
        doc,
        "The research was conducted through an international multi-institutional collaborative consortium involving academic eye centers and pediatric hospitals: the Shiley Eye Institute at the University of California San Diego (UCSD) Health System, the California Retinal Consultants, Medical Center Ophthalmology Associates, Guangzhou Women and Children's Medical Center, Beijing Tongren Eye Center, and Shanghai First People's Hospital. The study protocol was approved by the respective Institutional Review Boards (IRBs) of all participating institutions and complied fully with the Health Insurance Portability and Accountability Act (HIPAA) and the ethical principles of the Declaration of Helsinki. All patient records, image headers, and metadata were comprehensively de-identified prior to computational analysis.",
        bold_prefix="Multi-Center Consortium: "
    )

    add_heading_2(doc, "3.2 Retinal OCT Dataset Curation & CONSORT Stratification")
    add_body_p(
        doc,
        "The initial raw retinal image archive comprised 207,130 OCT B-scans collected from adult patients undergoing routine clinical evaluations between 2013 and 2017 using Spectralis OCT (Heidelberg Engineering) and Cirrus HD-OCT (Carl Zeiss Meditec) systems. To ensure rigorous data integrity, a multi-tier quality control protocol was deployed. Certified medical image graders and clinical specialists reviewed each B-scan, removing images with severe motion artifacts, extreme decentration, poor signal-to-noise ratio (< 15 dB), or ambiguous concurrent pathologies.",
        bold_prefix="Data Acquisition & Quality Control: "
    )
    add_body_p(
        doc,
        "Following strict quality filtering, 108,312 high-quality OCT images from 4,686 unique patients were curated for the primary experimental cohort. To ensure completely unbiased evaluation, an independent test set of 1,000 images (exactly 250 images per diagnostic category) was randomly extracted from 633 unique patients who were entirely excluded from model training and hyperparameter validation.",
        bold_prefix="Dataset Stratification: "
    )

    # Retinal OCT Dataset Distribution Table
    add_heading_3(doc, "Table 1: Distribution of Retinal OCT Dataset by Disease Category")
    oct_tbl = doc.add_table(rows=6, cols=5)
    oct_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    oct_tbl.autofit = False
    set_table_borders(oct_tbl, color="D3D9E2", sz="4", val="single")
    
    oct_cols = [Inches(1.8), Inches(1.3), Inches(1.1), Inches(1.1), Inches(1.2)]
    oct_headers = ["Diagnostic Category", "Clinical Triage Level", "Training Images", "Test Images", "Total Images"]
    
    # Header row
    hdr_row = oct_tbl.rows[0]
    for idx, name in enumerate(oct_headers):
        cell = hdr_row.cells[idx]
        cell.width = oct_cols[idx]
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(name)
        run.font.name = "Calibri"
        run.font.size = Pt(9.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    oct_data = [
        ("Choroidal Neovascularization (CNV)", "Urgent Referral", "37,206", "250", "37,456"),
        ("Diabetic Macular Edema (DME)", "Urgent Referral", "11,349", "250", "11,599"),
        ("Drusen (Dry AMD)", "Routine Referral", "8,617", "250", "8,867"),
        ("Normal Retina", "Routine Observation", "51,140", "250", "51,390"),
        ("Total Cohort", "All Triage Tiers", "108,312", "1,000", "109,312")
    ]
    for row_idx, r_data in enumerate(oct_data):
        row = oct_tbl.rows[row_idx + 1]
        bg = "F4F7FA" if row_idx % 2 == 1 else "FFFFFF"
        if row_idx == 4:
            bg = "E6EEF8"
        for col_idx, val in enumerate(r_data):
            cell = row.cells[col_idx]
            cell.width = oct_cols[col_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(val)
            run.font.name = "Calibri"
            run.font.size = Pt(9)
            if row_idx == 4:
                run.font.bold = True
                run.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
            else:
                run.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    sp_after_oct_tbl = doc.add_paragraph()
    sp_after_oct_tbl.paragraph_format.space_after = Pt(8)

    # Figure 2: Representative OCT Images & CONSORT Diagram
    add_figure_with_caption(
        doc,
        "extracted_figures/p5_img0_Im4.jpg",
        "Figure 2: Representative Retinal Optical Coherence Tomography Images and Data Curation Workflow.",
        "(A) Pathological B-scans: (Far left) Choroidal neovascularization (CNV) with hyperreflective neovascular membrane (white arrowheads) and extensive subretinal fluid (arrows). (Middle left) Diabetic macular edema (DME) showing massive neuroretinal thickening and intraretinal cystoid fluid cavities (arrows). (Middle right) Drusen present in early AMD, exhibiting discrete sub-RPE nodular elevations (arrowheads). (Far right) Normal retina with intact stratified cytoarchitecture and prominent foveal contour. (B) CONSORT-style flow diagram illustrating multi-stage data curation, quality exclusion filtering, and independent test cohort partitioning.",
        width_inches=5.8
    )

    add_heading_2(doc, "3.3 Pediatric Chest Radiography Cohort")
    add_body_p(
        doc,
        "To test the universal applicability of the transfer-learning framework, an independent dataset of 5,856 anterior-posterior pediatric chest radiographs from children aged one to five years was obtained from Guangzhou Women and Children's Medical Center. All images were acquired as part of standard clinical care and reviewed by pediatric radiologists.",
        bold_prefix="Pediatric X-Ray Cohort: "
    )
    add_body_p(
        doc,
        "The cohort was partitioned into a training set of 5,232 images (comprising 3,883 pneumonia cases [2,538 bacterial pneumonia, 1,345 viral pneumonia] and 1,349 normal control radiographs) and an independent test set of 624 images (comprising 390 pneumonia cases [242 bacterial, 148 viral] and 234 normal radiographs). Quality assessment excluded low-exposure, severely rotated, or motion-blurred scans.",
        bold_prefix="X-Ray Partitioning: "
    )

    add_heading_2(doc, "3.4 Deep Learning Architecture & Transfer Learning Strategy")
    add_body_p(
        doc,
        "The core computational model was instantiated using the Inception-V3 convolutional neural network architecture (Szegedy et al., 2016), pre-trained on the ImageNet large-scale visual recognition challenge dataset (1.28 million natural images spanning 1,000 distinct semantic categories). Inception-V3 incorporates factorized convolutions, multi-scale filter banks (1×1, 3×3, and 5×5 kernels), asymmetric convolutions (1×7 and 7×1), and auxiliary classification heads to mitigate gradient vanishing.",
        bold_prefix="Base Network Architecture: "
    )
    add_body_p(
        doc,
        "Crucially, the experimental methodology evaluated the trade-off between full end-to-end retraining versus transfer-learning feature adaptation. The authors experimentally established that backpropagating gradient updates throughout all layers on medical images rapidly resulted in severe overfitting and decreased test-set accuracy due to the immense parameter capacity (~23.8 million parameters) relative to clinical sample sizes. Consequently, the optimal transfer-learning paradigm froze all foundational convolutional and pooling layers, preserving the universal visual representations learned on ImageNet.",
        bold_prefix="The Freezing vs. Fine-Tuning Paradigm: "
    )
    add_body_p(
        doc,
        "The original 1,000-class ImageNet softmax classification head was excised and replaced with a custom-designed medical diagnostic head comprising: (1) a global average pooling layer, (2) a fully connected dense layer (1,024 units with ReLU activation), (3) a dropout regularization layer (dropout probability = 0.5) to prevent co-adaptation of feature detectors, and (4) a final linear classification layer mapped via softmax activation to K output probabilities (where K = 4 for retinal OCT, and K = 2 for chest X-ray binary tasks).",
        bold_prefix="Custom Classification Head: "
    )
    add_body_p(
        doc,
        "Models were trained using categorical cross-entropy loss:\n"
        "L = -SUM_i SUM_k y_ik * log(p_ik)\n"
        "where y_ik represents ground-truth one-hot indicators and p_ik represents predicted class probabilities. Optimization was performed using RMSprop with an initial learning rate of 0.001, momentum of 0.9, and exponential learning rate decay. Real-time data augmentation was applied during training—including random horizontal flipping, subtle contrast adjustments (±10%), and small affine scalings (±5%)—to simulate clinical imaging variability without distorting anatomical spatial integrity.",
        bold_prefix="Mathematical Optimization & Augmentation: "
    )

    add_heading_2(doc, "3.5 Human Ophthalmology Expert Benchmark Protocol")
    add_body_p(
        doc,
        "To rigorously contextualize algorithmic performance within real-world clinical standards, six board-certified ophthalmologists were recruited to evaluate the exact same 1,000-image OCT test cohort under identical, blinded conditions. The human expert panel was stratified by clinical subspecialty experience:",
        bold_prefix="Human Panel Stratification: "
    )
    add_bullet_p(doc, "Fellowship-trained vitreoretinal subspecialists with 10 to 20+ years of dedicated clinical practice in medical retina and macular surgery.", bold_prefix="Experts 1, 2, and 3: ")
    add_bullet_p(doc, "Certified general ophthalmologists and senior clinical fellows actively interpreting OCT scans in general ophthalmic practice.", bold_prefix="Experts 4, 5, and 6: ")
    add_body_p(
        doc,
        "The human ophthalmologists evaluated the 1,000 B-scans independently without access to patient medical histories, clinical records, systemic disease status, visual acuity measurements, or past OCT examinations, replicating the exact information boundary available to the deep learning algorithm.",
        bold_prefix="Blinded Evaluation Protocol: "
    )
    add_body_p(
        doc,
        "Standard classification accuracy measures every misclassification equally. However, in clinical medicine, diagnostic errors carry drastically asymmetric prognostic consequences. Misclassifying an urgent, treatable vision-threatening condition (CNV or DME) as normal is catastrophic: the patient is sent away without care, resulting in irreversible photoreceptor death and permanent blindness within weeks. Conversely, misclassifying a normal scan as urgent causes temporary patient anxiety and an unnecessary clinic visit, but does not result in physical organ damage. To reflect this reality, the authors formulated a Clinical Weighted Error Penalty Score:",
        bold_prefix="Clinical Weighted Error Score Formulation: "
    )
    add_bullet_p(doc, "Urgent referral (CNV or DME) misclassified as Normal (High clinical risk: missed sight-saving therapy).", bold_prefix="Penalty Weight = 4: ")
    add_bullet_p(doc, "Urgent referral (CNV or DME) misclassified as Drusen (Moderate clinical risk: routine referral delays treatment).", bold_prefix="Penalty Weight = 2: ")
    add_bullet_p(doc, "All other incorrect classification assignments (e.g., Drusen as Normal, Normal as Drusen, Normal as Urgent).", bold_prefix="Penalty Weight = 1: ")
    add_bullet_p(doc, "Correct diagnostic assignment matching gold-standard consensus.", bold_prefix="Penalty Weight = 0: ")

    add_heading_2(doc, "3.6 Algorithmic Interpretability via Occlusion Sensitivity Mapping")
    add_body_p(
        doc,
        "A profound critique of deep learning in clinical medicine is the 'black box' dilemma—the inability of clinicians to determine whether algorithmic predictions reflect genuine biological pathology or spurious image artifacts (such as border clipping, vignetting, or device brand watermarks). To establish transparent algorithmic explainability, the authors implemented Occlusion Sensitivity Mapping (Zeiler & Fergus, 2014).",
        bold_prefix="The Interpretability Challenge: "
    )
    add_body_p(
        doc,
        "A neutral grey occluding kernel of dimension N x N pixels (e.g., 30 x 30 pixels) was systematically translated across the input B-scan in a raster-scan grid with a stride of S pixels. At each coordinate (x, y), the neural network re-calculated the posterior class probability for the ground-truth category. The differential probability drop:\n"
        "Delta P(x, y) = P(ground_truth | original_image) - P(ground_truth | occluded_at_xy)\n"
        "was recorded. When the occluder covers a feature critical to the diagnosis, Delta P spikes dramatically. Normalizing these probability drops across the 2D spatial coordinates generates a continuous heatmap where pixel intensities directly map the spatial importance attributed by the neural network to underlying biological structures.",
        bold_prefix="Occlusion Mapping Mechanics: "
    )

    add_heading_2(doc, "3.7 Statistical Analysis & Evaluation Metrics")
    add_body_p(
        doc,
        "Diagnostic performance was quantitatively evaluated across established epidemiological and biostatistical metrics: Accuracy, Sensitivity (True Positive Rate), Specificity (True Negative Rate), Positive Predictive Value (Precision), Negative Predictive Value, and Receiver Operating Characteristic (ROC) curves. The Area Under the ROC Curve (AUC) was computed via trapezoidal integration. Two-sided 95% Confidence Intervals (CIs) were determined using Clopper-Pearson exact binomial intervals for sensitivities and specificities, and DeLong's non-parametric method for AUCs. Positive Likelihood Ratios (LR+ = Sensitivity / [1 - Specificity]) and Negative Likelihood Ratios (LR- = [1 - Sensitivity] / Specificity) were evaluated to assess clinical diagnostic utility.",
        bold_prefix="Statistical Formulations: "
    )

    # -------------------------------------------------------------
    # 4. RESULTS
    # -------------------------------------------------------------
    add_heading_1(doc, "4. RESULTS")
    
    add_heading_2(doc, "4.1 Retinal Optical Coherence Tomography Performance")
    add_body_p(
        doc,
        "The deep learning transfer framework demonstrated extraordinary diagnostic performance across all retinal evaluation benchmarks. In initial binary classification tasks, the model segregated pathological states from normal healthy retinas with near-perfect fidelity:",
        bold_prefix="Binary Diagnostic Classifications: "
    )
    add_bullet_p(doc, "Achieved an accuracy of 100.0%, sensitivity of 100.0%, specificity of 100.0%, and an Area Under the ROC Curve (AUC) of 100.0% (1.000).", bold_prefix="Choroidal Neovascularization vs. Normal: ")
    add_bullet_p(doc, "Achieved an accuracy of 98.2%, sensitivity of 96.8%, specificity of 99.6%, and an AUC of 99.87% (0.9987).", bold_prefix="Diabetic Macular Edema vs. Normal: ")
    add_bullet_p(doc, "Achieved an accuracy of 94.8%, sensitivity of 91.2%, specificity of 98.4%, and an AUC of 99.1% (0.991).", bold_prefix="Drusen vs. Normal: ")

    add_body_p(
        doc,
        "In the primary multi-class clinical triage task—where the model had to concurrently categorize test B-scans across all four mutually exclusive diagnostic classes—the system attained an overall accuracy of 96.6%, with an overall sensitivity of 97.8% and specificity of 97.4%. When evaluating the critical clinical triage cutoff for 'Urgent Referrals' (detecting patients with active CNV or DME requiring immediate anti-VEGF intervention versus routine drusen/normal cases), the deep-learning algorithm achieved an astonishing Area Under the ROC Curve of 99.9% (AUC = 0.999; 95% CI: 0.998–1.000).",
        bold_prefix="Multi-Class Clinical Referral Performance: "
    )

    # Table 2: Diagnostic Performance Metrics Table
    add_heading_3(doc, "Table 2: Diagnostic Performance Summary for Retinal OCT & Chest Radiography")
    res_tbl = doc.add_table(rows=6, cols=6)
    res_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    res_tbl.autofit = False
    set_table_borders(res_tbl, color="D3D9E2", sz="4", val="single")
    
    res_cols = [Inches(1.8), Inches(1.0), Inches(0.9), Inches(0.9), Inches(0.9), Inches(1.0)]
    res_headers = ["Clinical Task / Modality", "Accuracy", "Sensitivity", "Specificity", "AUC", "Clinical Impact"]
    
    hdr_row2 = res_tbl.rows[0]
    for idx, name in enumerate(res_headers):
        cell = hdr_row2.cells[idx]
        cell.width = res_cols[idx]
        set_cell_background(cell, "1B365D")
        set_cell_margins(cell, top=80, bottom=80, left=60, right=60)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(name)
        run.font.name = "Calibri"
        run.font.size = Pt(9.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    res_data = [
        ("OCT: CNV vs. Normal", "100.0%", "100.0%", "100.0%", "100.0%", "Urgent Triage"),
        ("OCT: DME vs. Normal", "98.2%", "96.8%", "99.6%", "99.87%", "Urgent Triage"),
        ("OCT: Drusen vs. Normal", "94.8%", "91.2%", "98.4%", "99.10%", "Routine Triage"),
        ("OCT: Urgent Referrals (CNV+DME)", "96.6%", "97.8%", "97.4%", "99.90%", "Sight Preservation"),
        ("CXR: Pneumonia vs. Normal", "92.8%", "93.2%", "90.1%", "96.80%", "Infection Triage"),
        ("CXR: Bacterial vs. Viral Pneumonia", "90.7%", "88.6%", "90.9%", "94.00%", "Antibiotic Stewardship")
    ]
    for row_idx, r_data in enumerate(res_data):
        row = res_tbl.rows[row_idx + 1] if row_idx < 5 else res_tbl.add_row()
        bg = "F4F7FA" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(r_data):
            cell = row.cells[col_idx]
            cell.width = res_cols[col_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(val)
            run.font.name = "Calibri"
            run.font.size = Pt(9)
            run.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    sp_after_res_tbl = doc.add_paragraph()
    sp_after_res_tbl.paragraph_format.space_after = Pt(8)

    # Figure 4: Multi-Class Comparison ROC, Confusion Matrix & Expert Benchmark
    add_figure_with_caption(
        doc,
        "extracted_figures/p6_img0_Im5.jpg",
        "Figure 4: Multi-Class Diagnostic Performance and Benchmark Comparison Against Human Experts.",
        "(A) Receiver Operating Characteristic (ROC) curve for urgent referral triage (detecting CNV and DME against Drusen and Normal). The Area Under the Curve (AUC) reached 99.9% (solid curve). Individual diagnostic operating points for six human ophthalmologists are plotted, demonstrating that the AI system matches or exceeds human expert sensitivity and specificity. (B) Multi-class confusion matrix of the deep learning model across 1,000 independent test images (250 per class). (C) Clinical Weighted Error Score comparison: the deep learning model (gold bar, error score = 0.112) outperformed all six board-certified human ophthalmologists (blue bars, error scores ranging from 0.116 to 0.230).",
        width_inches=5.8
    )

    add_heading_2(doc, "4.2 Comparison Against Six Human Ophthalmology Experts")
    add_body_p(
        doc,
        "Direct clinical benchmarking revealed that the deep-learning algorithm matched the diagnostic accuracy of the most experienced senior vitreoretinal specialists and substantially outperformed general ophthalmologists. When evaluating the clinical weighted error metric (which penalizes false-negative urgent referrals heavily):",
        bold_prefix="Human-Machine Benchmark: "
    )
    add_bullet_p(doc, "The deep learning model achieved the lowest (best) weighted error score of 0.112.", bold_prefix="Deep Learning System: ")
    add_bullet_p(doc, "Senior vitreoretinal specialists achieved weighted error scores of 0.116 (Expert 1), 0.134 (Expert 2), and 0.142 (Expert 3).", bold_prefix="Retinal Subspecialists (Experts 1–3): ")
    add_bullet_p(doc, "General ophthalmologists and clinical fellows attained weighted error scores of 0.198 (Expert 4), 0.214 (Expert 5), and 0.230 (Expert 6).", bold_prefix="General Ophthalmologists (Experts 4–6): ")
    add_body_p(
        doc,
        "The model demonstrated a positive likelihood ratio (LR+) exceeding 37.6 for urgent referral triage, establishing outstanding 'rule-in' diagnostic capability. Concurrently, its negative likelihood ratio (LR-) was below 0.023, confirming extraordinary 'rule-out' clinical power, ensuring virtually no sight-threatening cases are mistakenly dismissed.",
        bold_prefix="Clinical Likelihood Ratios: "
    )

    add_heading_2(doc, "4.3 Algorithmic Explainability & Anatomical Feature Verification")
    add_body_p(
        doc,
        "Occlusion sensitivity heatmaps provided unequivocal biological validation of the deep neural network's internal representations, confirming that the model's high accuracy did not stem from background artifacts or peripheral noise:",
        bold_prefix="Pathological Concordance of Saliency Maps: "
    )
    add_bullet_p(
        doc,
        "In CNV images, peak occlusion sensitivity localized strictly to the subretinal space, precisely overlying the hyperreflective fibrovascular membrane and adjacent pockets of hyporeflective subretinal fluid exudation.",
        bold_prefix="Choroidal Neovascularization: "
    )
    add_bullet_p(
        doc,
        "In DME images, peak sensitivity mapped directly to intraretinal cystoid hyporeflective spaces within the outer plexiform and inner nuclear layers, as well as diffuse macular swelling.",
        bold_prefix="Diabetic Macular Edema: "
    )
    add_bullet_p(
        doc,
        "In Drusen B-scans, occlusion sensitivity was intensely concentrated over the localized, dome-shaped elevations of the retinal pigment epithelium and underlying sub-RPE deposits.",
        bold_prefix="Drusen: "
    )
    add_bullet_p(
        doc,
        "Normal retinal scans demonstrated low-magnitude, diffuse, homogeneous background attention distributed evenly along the healthy foveal depression without focal anatomical fixation.",
        bold_prefix="Normal Control Scans: "
    )

    # Figure 5: Occlusion Maps & Longitudinal Anti-VEGF Follow-up
    add_figure_with_caption(
        doc,
        "extracted_figures/p8_img0_Im6.jpg",
        "Figure 5: Occlusion Sensitivity Saliency Maps and Longitudinal Anti-VEGF Therapeutic Tracking.",
        "(A) Heatmaps generated via occlusion sensitivity mapping for Diabetic Macular Edema (left), Choroidal Neovascularization (middle), and Drusen (right). Hot zones (red/yellow) indicate anatomical coordinates whose occlusion produced the steepest collapse in diagnostic confidence, validating that the network focuses strictly on genuine biological pathology. (B) Longitudinal B-scans and accompanying occlusion maps in a patient with CNV undergoing anti-VEGF pharmacotherapy. Pre-treatment scans exhibit extensive subretinal fluid and prominent occlusion peaks. Following anti-VEGF injection, follow-up scans demonstrate progressive fluid resorption, structural retinal flattening, and concomitant dissipation of occlusion saliency.",
        width_inches=5.8
    )

    add_heading_2(doc, "4.4 Longitudinal Monitoring of Anti-VEGF Pharmacotherapy")
    add_body_p(
        doc,
        "Beyond single-timepoint diagnostic classification, the experimental investigation demonstrated that the deep learning system can objectively track disease progression and therapeutic response over time. Patients presenting with active exudative CNV were imaged longitudinally prior to and following intravitreal anti-VEGF pharmacotherapy. Prior to treatment, baseline B-scans showed marked subretinal fluid elevation, which the AI model categorized as CNV with >99% confidence and prominent occlusion heatmap activation.",
        bold_prefix="Longitudinal Therapeutic Tracking: "
    )
    add_body_p(
        doc,
        "Following intravitreal anti-VEGF therapy (at week 4 and week 8 post-injection), subsequent OCT B-scans demonstrated progressive re-absorption of subretinal fluid, resolution of macular edema, and flattening of the neurosensory detachment. Crucially, the AI model's occlusion heatmaps quantitatively mirrored this clinical recovery: the intensity and spatial footprint of the pathological focus progressively diminished, transitioning toward a quiescent structural profile. This finding proves that transfer-learning AI models can serve as automated, objective tools for monitoring therapeutic efficacy and detecting disease recurrence.",
        bold_prefix="Quantitative Remodeling Tracking: "
    )

    add_heading_2(doc, "4.5 Generalization to Pediatric Pneumonia Detection & Etiological Differentiation")
    add_body_p(
        doc,
        "A critical milestone of this experiential research was establishing that a transfer-learning framework developed for micro-scale ophthalmological tomograms could generalize effectively to macro-scale projection radiographs in pediatric emergency pulmonology without changing the underlying architecture.",
        bold_prefix="Cross-Disciplinary Translation: "
    )
    add_body_p(
        doc,
        "On the independent test cohort of 624 pediatric chest radiographs, the deep learning model achieved an overall accuracy of 92.8%, a sensitivity of 93.2%, a specificity of 90.1%, and an Area Under the ROC Curve of 96.8% (AUC = 0.968) in distinguishing pneumonia from healthy pediatric lung parenchyma. This performance establishes that the model can serve as a dependable triage tool in busy pediatric emergency departments.",
        bold_prefix="Pneumonia Screening Performance: "
    )
    add_body_p(
        doc,
        "Even more clinically significant was the model's ability to tackle the formidable diagnostic challenge of etiological classification: differentiating bacterial pneumonia from viral pneumonia. Bacterial pneumonia typically manifests as focal, dense lobar or segmental consolidation, whereas viral pneumonia presents with diffuse, bilateral interstitial or bronchopneumonic infiltrates. In differentiating bacterial from viral pneumonia, the transfer-learning model attained an accuracy of 90.7%, a sensitivity of 88.6%, a specificity of 90.9%, and an AUC of 94.0% (AUC = 0.940). This high diagnostic discrimination provides vital clinical decision support for pediatricians, promoting timely antibiotic administration for bacterial infections while preventing unnecessary antibiotic prescriptions in viral cases.",
        bold_prefix="Bacterial vs. Viral Etiological Differentiation: "
    )

    # Figure 6: Pediatric Chest X-Ray Performance
    add_figure_with_caption(
        doc,
        "extracted_figures/p9_img0_Im7.jpg",
        "Figure 6: Diagnostic Performance of the Transfer Learning Model on Pediatric Chest Radiographs.",
        "(A-B) Training and validation accuracy (A) and cross-entropy loss (B) over 10,000 steps for pneumonia vs. normal classification. (C-D) Training and validation accuracy (C) and loss (D) for binary classification between bacterial pneumonia and viral pneumonia. (E) Receiver Operating Characteristic (ROC) curve and confusion matrix for detecting pneumonia versus normal lungs (AUC = 96.8%). (F) ROC curve and confusion matrix for differentiating bacterial pneumonia from viral pneumonia (AUC = 94.0%).",
        width_inches=5.8
    )

    # Figure S6: Clinical Examples of Chest X-Rays
    add_figure_with_caption(
        doc,
        "extracted_figures/rgb_p20_img0_Im6.jpg",
        "Figure S6: Illustrative Pathological Chest Radiographs from Pediatric Patients.",
        "(Left panel) Normal pediatric chest radiograph depicting clear lung fields, sharp costophrenic angles, and normal cardiothoracic ratio. (Middle panel) Bacterial pneumonia presenting with focal lobar consolidation in the right upper lobe (white arrows). (Right panel) Viral pneumonia demonstrating diffuse, bilateral interstitial infiltrates and peribronchial thickening throughout both lung fields.",
        width_inches=5.8
    )

    # -------------------------------------------------------------
    # 5. CONCLUSION & EXPERIENTIAL LEARNING INSIGHTS
    # -------------------------------------------------------------
    add_heading_1(doc, "5. CONCLUSION & EXPERIENTIAL LEARNING INSIGHTS")
    
    add_heading_2(doc, "5.1 Synthesis of Scientific Contributions")
    add_body_p(
        doc,
        "This landmark investigation establishes that transfer learning provides a robust, clinically viable solution to the fundamental data scarcity bottleneck that has historically impeded medical artificial intelligence. By transferring foundational visual representations from 1.28 million natural images (ImageNet) to clinical imaging cohorts, deep convolutional neural networks can achieve diagnostic performance comparable to, and in some metrics exceeding, senior human medical subspecialists.",
        bold_prefix="Overcoming the Data Scarcity Bottleneck: "
    )
    add_body_p(
        doc,
        "The study's successful translation across two completely disparate clinical fields—microscopic optical coherence tomography in adult ophthalmology and macroscopic projection radiography in pediatric emergency pulmonology—demonstrates that the transfer learning methodology is an extensible, generalized diagnostic platform rather than an overfitted domain-specific model.",
        bold_prefix="Universal Cross-Disciplinary Generalization: "
    )

    add_heading_2(doc, "5.2 Clinical Translation & Global Healthcare Equality")
    add_body_p(
        doc,
        "The translational implications of this research are profound, directly addressing acute disparities in global healthcare access:",
        bold_prefix="Democratizing Specialized Healthcare: "
    )
    add_bullet_p(
        doc,
        "In developing nations and rural communities where vitreoretinal surgeons and pediatric radiologists are scarce, deploying automated transfer-learning triage algorithms on cloud or edge platforms enables rapid point-of-care screening. Patients with treatable vision-threatening conditions (CNV, DME) can be flagged and referred immediately, preventing irreversible blindness.",
        bold_prefix="Rural & Underserved Access: "
    )
    add_bullet_p(
        doc,
        "Childhood pneumonia claims nearly one million lives each year primarily in resource-limited settings. Automated differentiation of bacterial from viral pneumonia on plain radiographs enables healthcare workers to administer antibiotics promptly when indicated while adhering to strict antibiotic stewardship, mitigating the catastrophic rise of antimicrobial-resistant superbugs.",
        bold_prefix="Pediatric Antibiotic Stewardship: "
    )
    add_bullet_p(
        doc,
        "Rather than replacing physicians, this AI framework establishes a collaborative 'Human-in-the-Loop' clinical decision support architecture. Automating routine normal scans and straightforward drusen frees specialized clinicians to focus their time and cognitive resources on complex surgical and therapeutic interventions.",
        bold_prefix="Decision Support vs. Replacement: "
    )

    add_heading_2(doc, "5.3 Experiential Learning Takeaways for Biology & Biomedical Engineering")
    add_body_p(
        doc,
        "Engaging deeply with this Cell research provides crucial experiential learning principles for students, researchers, and practitioners at the intersection of biological sciences and artificial intelligence:",
        bold_prefix="Key Educational Takeaways: "
    )
    add_bullet_p(
        doc,
        "Algorithms cannot be treated as abstract mathematical functions; they must be grounded in underlying cellular and tissue pathophysiology. Understanding the biological mechanisms of VEGF-mediated choroidal neovascularization, diabetic capillary hyperpermeability, and bacterial alveolar consolidation was essential to defining clinical triage tiers and penalty scoring matrices.",
        bold_prefix="1. Deep Integration of Biological Pathophysiology: "
    )
    add_bullet_p(
        doc,
        "Standard machine learning metrics (such as unweighted accuracy or macro-F1 score) are fundamentally inadequate in medical diagnosis. In healthcare, false negatives and false positives have profoundly asymmetric human costs. Formulating domain-specific clinical weighted error scores that heavily penalize missed vision-threatening conditions represents an essential paradigm shift for clinical data science.",
        bold_prefix="2. The Imperative of Clinical Weighted Metrics: "
    )
    add_bullet_p(
        doc,
        "The deployment of occlusion sensitivity mapping proved that neural networks can be demystified. Confirming that algorithmic focus precisely aligns with biological fluid pockets, neovascular membranes, and infiltrates is a non-negotiable prerequisite for clinician trust, regulatory approval (FDA/CE mark), and patient safety.",
        bold_prefix="3. Transparency & Algorithmic Explainability: "
    )
    add_bullet_p(
        doc,
        "The study adhered to exceptional standards of open science by publicly depositing the entire dataset of over 100,000 OCT B-scans and pediatric radiographs, along with complete network architectures and pre-trained weights. Open data sharing accelerates reproducible research and powers continuous collaborative innovation across the global scientific community.",
        bold_prefix="4. Open Science & Reproducible Benchmarking: "
    )

    add_heading_2(doc, "5.4 Limitations & Future Trajectories")
    add_body_p(
        doc,
        "While this study represents a watershed achievement, several important limitations highlight trajectories for future research: (1) The retrospective nature of the image cohorts warrants prospective clinical trials in real-world primary care settings to assess diagnostic accuracy in live patient workflows; (2) The current architecture evaluated single 2D B-scans rather than whole 3D volumetric OCT cubes or multi-view chest radiographs; (3) Future models should integrate multi-modal clinical data—incorporating genetic biomarkers, optical coherence tomography angiography (OCTA) vascular flow maps, clinical laboratory tests, and electronic health records (EHR) into a unified predictive diagnostic network.",
        bold_prefix="Future Horizons: "
    )

    # -------------------------------------------------------------
    # 6. REFERENCES
    # -------------------------------------------------------------
    add_heading_1(doc, "6. REFERENCES")
    
    add_heading_2(doc, "6.1 Primary Landmark Study Citation")
    add_body_p(
        doc,
        "Kermany, D.S., Goldbaum, M., Cai, W., Valentim, C.C.S., Liang, H., Baxter, S.L., McKeown, A., Yang, G., Wu, X., Yan, F., Dong, J., Prasad, M.K., Pei, J., Ting, M.Y.Z., Li, C., Hewing, S., Dong, L., Ayres, I., Zhang, D., Holmes, J.P., and Zhang, K. (2018). Identifying Medical Diagnoses and Treatable Diseases by Image-Based Deep Learning. Cell 172(5), 1122–1131.e9. https://doi.org/10.1016/j.cell.2018.02.010",
        bold_prefix="[1] "
    )

    add_heading_2(doc, "6.2 Cited Literature in Kermany et al. (Original Study Citations)")
    
    study_refs = [
        "Adegbola, R.A. (2012). Childhood pneumonia as a global health priority and the strategic interest of the Bill & Melinda Gates Foundation. Clin. Infect. Dis. 54(Suppl 2), S89–S92.",
        "Chaudhuri, S., Chatterjee, S., Katz, N., Nelson, M., and Goldbaum, M. (1989). Detection of blood vessels in retinal images using two-dimensional matched filters. IEEE Trans. Med. Imaging 8, 263–269.",
        "Donahue, J., Jia, Y., Vinyals, O., Hoffman, J., Zhang, N., Tzeng, E., and Darrell, T. (2013). DeCAF: A Deep Convolutional Activation Feature for Generic Visual Recognition. Proceedings of the 31st International Conference on Machine Learning 32, 647–655.",
        "Ferrara, N. (2010). Vascular endothelial growth factor and age-related macular degeneration: from basic science to therapy. Nat. Med. 16, 1107–1111.",
        "Friedman, D.S., O'Colmain, B.J., Muñoz, B., Tomany, S.C., McCarty, C., de Jong, P.T., Nemesure, B., Mitchell, P., and Kempen, J.; Eye Diseases Prevalence Research Group (2004). Prevalence of age-related macular degeneration in the United States. Arch. Ophthalmol. 122, 564–572.",
        "Goldbaum, M., Moezzi, S., Taylor, A., Chatterjee, S., Boyd, J., Hunter, E., and Jain, R. (1996). Automated diagnosis and image understanding with object extraction, object classification, and inferencing in retinal images. Proceedings of 3rd IEEE International Conference on Image Processing 3, 695–698.",
        "Gulshan, V., Peng, L., Coram, M., Stumpe, M.C., Wu, D., Narayanaswamy, A., Venugopalan, S., Widner, K., Madams, T., Cuadros, J., et al. (2016). Development and Validation of a Deep Learning Algorithm for Detection of Diabetic Retinopathy in Retinal Fundus Photographs. JAMA 316, 2402–2410.",
        "Hoover, A., and Goldbaum, M. (2003). Locating the optic nerve in a retinal image using the fuzzy convergence of the blood vessels. IEEE Trans. Med. Imaging 22, 951–958.",
        "Hoover, A., Kouznetsova, V., and Goldbaum, M. (2000). Locating blood vessels in retinal images by piecewise threshold probing of a matched filter response. IEEE Trans. Med. Imaging 19, 203–210.",
        "Kaiser, P.K., Brown, D.M., Zhang, K., Hudson, H.L., Holz, F.G., Shapiro, H., Schneider, S., and Acharya, N.R. (2007). Ranibizumab for predominantly classic neovascular age-related macular degeneration: subgroup analysis of first-year ANCHOR results. Am. J. Ophthalmol. 144, 850–857.",
        "Krizhevsky, A., Sutskever, I., and Hinton, G.E. (2017). ImageNet classification with deep convolutional neural networks. Commun. ACM 60, 84–90.",
        "Lee, C.S., Baughman, D.M., and Lee, A.Y. (2016). Deep Learning Is Effective for the Classification of OCT Images of Normal versus Age-Related Macular Degeneration. Ophthalmol. Retina 1, 322–327.",
        "Mcluckie, A. (2009). Respiratory disease and its management, Volume 57 (Springer).",
        "Razavian, A.S., Azizpour, H., Sullivan, J., and Carlsson, S. (2014). CNN Features Off-the-Shelf: An Astounding Baseline for Recognition. In 2014 IEEE Conference on Computer Vision and Pattern Recognition Workshops, pp. 512–519.",
        "Rudan, I., Boschi-Pinto, C., Biloglav, Z., Mulholland, K., and Campbell, H. (2008). Epidemiology and etiology of childhood pneumonia. Bull. World Health Organ. 86, 408–416.",
        "Swanson, E.A., and Fujimoto, J.G. (2017). The ecosystem that powered the translation of OCT from fundamental research to clinical and commercial impact. Biomed. Opt. Express 8, 1638–1664.",
        "Szegedy, C., Vanhoucke, V., Ioffe, S., Shlens, J., and Wojna, Z. (2016). Rethinking the Inception Architecture for Computer Vision. In 2016 IEEE Conference on Computer Vision and Pattern Recognition, pp. 2818–2826.",
        "Varma, R., Bressler, N.M., Doan, Q.V., Gleeson, M., Danese, M., Bower, J.K., Selvin, E., Dolan, C., Fine, J., Colman, S., and Turpcu, A. (2014). Prevalence of and risk factors for diabetic macular edema in the United States. JAMA Ophthalmol. 132, 1334–1340.",
        "Wong, W.L., Su, X., Li, X., Cheung, C.M., Klein, R., Cheng, C.Y., and Wong, T.Y. (2014). Global prevalence of age-related macular degeneration and disease burden projection for 2020 and 2040: a systematic review and meta-analysis. Lancet Glob. Health 2, e106–e116.",
        "Yosinski, J., Clune, J., Bengio, Y., and Lipson, H. (2014). How transferable are features in deep neural networks? In NIPS'14 Proceedings of the 27th International Conference on Neural Information Processing Systems, pp. 3320–3328.",
        "Zeiler, M.D., and Fergus, R. (2014). Visualizing and Understanding Convolutional Networks. In Computer Vision – ECCV 2014, Lecture Notes in Computer Science, Volume 8689 (Springer), pp. 818–833."
    ]
    for idx, ref in enumerate(study_refs):
        add_body_p(doc, ref, bold_prefix=f"[{idx+2}] ")

    add_heading_2(doc, "6.3 Cell Companion Commentary Citation")
    add_body_p(
        doc,
        "Schmidt-Erfurth, U., Sadeghipour, A., Gerendas, B.S., and Waldstein, S.M. (2018). Learning from Everyday Images Enables Expert-like Diagnosis of Retinal Diseases. Cell 172(5), 893–895. https://doi.org/10.1016/j.cell.2018.02.013",
        bold_prefix="[23] "
    )

    add_heading_2(doc, "6.4 Comprehensive Cell Press Repository Bibliography (Companion Folder Articles)")
    add_body_p(
        doc,
        "The following peer-reviewed articles constitute the comprehensive Cell Press research repository provided in the project archive ('Cell Press_20260927'), providing the broader contextual ecosystem across computational oncology, neuroscience, genetics, cellular microbiology, and structural biology:",
        bold_prefix="Repository Context: "
    )

    cell_folder_refs = [
        ("Oncology & Cancer Biology", [
            ("A-Hematogenous-Route-for-Medulloblastoma-Leptomeni.pdf", "Garzia, L. et al. (2018). A Hematogenous Route for Medulloblastoma Leptomeningeal Metastases. Cell 172(5), 1050–1062."),
            ("NK-Cells-Stimulate-Recruitment-of-cDC1-into-the-Tu.pdf", "Böttcher, J.P. et al. (2018). NK Cells Stimulate Recruitment of cDC1 into the Tumor Microenvironment Promoting Cancer Immune Control. Cell 172(5), 1022–1037.")
        ]),
        ("Neurobiology, Brain Plasticity & Neurodevelopment", [
            ("A-Mild-PUM1-Mutation-Is-Associated-with-Adult-Onse.pdf", "Gennarino, V.A. et al. (2018). A Mild PUM1 Mutation Is Associated with Adult-Onset Ataxia, whereas Haploinsufficiency Causes Developmental Delay and Seizures. Cell 172(5), 924–936."),
            ("Cell-Intrinsic-Control-of-Interneuron-Migration-Dr.pdf", "Silva, C.G. et al. (2018). Cell-Intrinsic Control of Interneuron Migration Drives Cortical Morphogenesis. Cell 172(5), 1063–1078."),
            ("Dissecting-the-Causal-Mechanism-of-X-Linked-Dyston.pdf", "Aneichyk, T. et al. (2018). Dissecting the Causal Mechanism of X-Linked Dystonia-Parkinsonism by Integrating Genome and Transcriptome Assembly. Cell 172(5), 897–909."),
            ("Rescue-of-Fragile-X-Syndrome-Neurons-by-DNA-Methyl.pdf", "Liu, X.S. et al. (2018). Rescue of Fragile X Syndrome Neurons by DNA Methylation Editing of the FMR1 Gene. Cell 172(5), 979–992."),
            ("Super-Resolution-Imaging-of-the-Extracellular-Spac.pdf", "Tønnesen, J. et al. (2018). Super-Resolution Imaging of the Extracellular Space in Living Brain Tissue. Cell 172(5), 1108–1121.")
        ]),
        ("Genetics, Epigenetics & Developmental Biology", [
            ("A-Non-catalytic-Function-of-SETD1A-Regulates-Cycli.pdf", "Hoshii, T. et al. (2018). A Non-catalytic Function of SETD1A Regulates Cyclin K and the DNA Damage Response. Cell 172(5), 1007–1021."),
            ("Direct-Identification-of-Hundreds-of-Expression-Mo.pdf", "Tewhey, R. et al. (2018). Direct Identification of Hundreds of Expression-Modulating Variants using a Multiplexed Reporter Assay. Cell 172(5), 1132–1134."),
            ("Identification-of-piRNA-Binding-Sites-Reveals-the-.pdf", "Shen, E.Z. et al. (2018). Identification of piRNA Binding Sites Reveals the Argonaute Regulatory Landscape of the C. elegans Germline. Cell 172(5), 937–951."),
            ("Inborn-Errors-of-RNA-Lariat-Metabolism-in-Humans-w.pdf", "Zhang, S.Y. et al. (2018). Inborn Errors of RNA Lariat Metabolism in Humans with Brainstem Viral Infection. Cell 172(5), 952–965."),
            ("Mapping-the-Mouse-Cell-Atlas-by-Microwell-Seq_cell.pdf", "Han, X. et al. (2018). Mapping the Mouse Cell Atlas by Microwell-Seq. Cell 172(5), 1091–1107."),
            ("Modulation-of-Phase-Shift-between-Wnt-and-Notch-Si.pdf", "Sonnen, K.F. et al. (2018). Modulation of Phase Shift between Wnt and Notch Signaling Oscillations Controls Mesoderm Segmentation. Cell 172(5), 1079–1090."),
            ("Pervasive,-Coordinated-Protein-Level-Changes-Drive.pdf", "Cheng, Z. et al. (2018). Pervasive, Coordinated Protein-Level Changes Driven by Transcript Isoform Switching during Meiosis. Cell 172(5), 910–923."),
            ("Placeholder-Nucleosomes-Underlie-Germline-to-Embry.pdf", "Murphy, P.J. et al. (2018). Placeholder Nucleosomes Underlie Germline-to-Embryo DNA Methylation Reprogramming. Cell 172(5), 993–1006."),
            ("Solving-Mendelian-Mysteries--The-Non-coding-Genome.pdf", "MacArthur, D.G. (2018). Solving Mendelian Mysteries: The Non-coding Genome May Hold the Key. Cell 172(5), 891–893.")
        ]),
        ("Microbiology, Virology & Antibiotic Resistance", [
            ("Antibiotic-Resistance_cell.pdf", "Blair, J.M.A. et al. (2018). Molecular Mechanisms of Antibiotic Resistance. Cell 172(5), 1136–1136.e1."),
            ("Electron-Cryo-microscopy-Structure-of-Ebola-Virus-.pdf", "Wan, W. et al. (2018). Electron Cryo-microscopy Structure of Ebola Virus Nucleoprotein Reveals a Mechanism for Nucleocapsid-like Assembly. Cell 172(5), 966–978."),
            ("Lysozyme-Counteracts-β-Lactam-Antibiotics-by-Promo.pdf", "Kawai, Y. et al. (2018). Lysozyme Counteracts Beta-Lactam Antibiotics by Promoting the Emergence of L-Form Bacteria. Cell 172(5), 1038–1049."),
            ("Retraction-Notice-to--(p)ppGpp-Controls-Bacterial-.pdf", "Cell Editorial Office (2018). Retraction Notice to: (p)ppGpp Controls Bacterial Persistence by Stochastic Induction of Toxin-Antitoxin Activity. Cell 172(5), 1135."),
            ("The-Unexpected-Effects-of-the-Combination-of-Antib.pdf", "Bollenbach, T. (2018). The Unexpected Effects of the Combination of Antibiotics and Immunity. Cell 172(5), 895–897.")
        ])
    ]

    start_idx = 24
    for cat_name, cat_articles in cell_folder_refs:
        add_heading_3(doc, cat_name)
        for pdf_name, citation in cat_articles:
            add_body_p(doc, f"{citation} [File: {pdf_name}]", bold_prefix=f"[{start_idx}] ")
            start_idx += 1

    # Save Document
    output_filename = "Biology_Experiential_Learning_Report_Cell_Deep_Learning.docx"
    doc.save(output_filename)
    print(f"Report successfully saved to: {output_filename}")
    return output_filename

if __name__ == "__main__":
    create_report()

