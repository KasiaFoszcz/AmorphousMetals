"""Introduction Streamlit subpage."""

import streamlit as st

from metale_amorficzne.streamlit.utils import get_image_path

st.title("Introduction")

st.header("Analyzer for Researchers at Wroclaw University of Science and Technology")
st.write(
    """
    The purpose of this study is to develop an _Amorphous Metals Analyzer_ specifically
    designed for researchers at Wroclaw University of Science and Technology. This
    analyzer aims to enhance the precision and efficiency of evaluating produced
    amorphous materials. By utilizing this tool, researchers can obtain more accurate
    and faster results regarding the number and properties of phases present in a given
    amorphous metal sample.
    """
)

st.header("Integration with Nanoindentation Machine")
st.write(
    """
    The Amorphous Metals Analyzer is integrated with a nanoindentation machine, which is
    capable of measuring various mechanical properties of the sample. The results
    obtained from the nanoindentation machine are fed into the analyzer, allowing for a
    comprehensive analysis of the material.
    """
)

st.header("Clustering of Metal Phases and Calculation of Mechanical Properties")
st.write(
    """
    Once the data from the nanoindentation machine is inputted into the analyzer, the
    application performs clustering of the different metal phases present in the sample.

    Furthermore, the Amorphous Metals Analyzer calculates key mechanical properties for
    each phase identified. These mechanical properties help researchers assess the
    quality and performance of the amorphous metal, providing valuable insights for
    further analysis and experimentation.

    Overall, the Amorphous Metals Analyzer serves as a tool for researchers at Wroclaw
    University of Science and Technology, enabling them to conduct faster evaluations of
    amorphous materials, contributing to advancements in material research and
    development.
    """
)

st.header("What are amorphous metals?")
st.write(
    """
    Amorphous metal also known as metallic glass or glassy metal is a solid metallic
    material, usually an alloy, with disordered atomic-scale structure.

    Most metals are crystalline in their solid state, which means they have a highly
    ordered arrangement of atoms. Amorphous metals are non-crystalline, and have a
    glass-like structure. But unlike common glasses, such as window glass, which are
    typically electrical insulators, amorphous metals have good electrical conductivity
    and can show metallic luster.
    """
)

st.image(
    get_image_path(__file__, "CrystalGrain.jpg"),
    caption="Microscopic image of traditional metal with grain boundaries",
)

st.image(
    get_image_path(__file__, "AmorphousMetal.jpg"),
    caption="Microscopic image of an amorphous metal",
)

st.write(
    """
    Amorphous metal alloys contain atoms of significantly different sizes, leading to
    low free volume (and therefore up to orders of magnitude higher viscosity than other
    metals and alloys) in molten state. The viscosity prevents the atoms moving enough
    to form an ordered lattice. The material structure also results in low shrinkage
    during cooling, and resistance to plastic deformation. The absence of grain
    boundaries, the weak spots of crystalline materials, leads to better resistance to
    wear and corrosion. Amorphous metals, while technically glasses, are also much
    tougher and less brittle than oxide glasses and ceramics. Amorphous metals can be
    grouped in two categories, as either non-ferromagnetic, if they are composed of Ln,
    Mg, Zr, Ti, Pd, Ca, Cu, Pt and Au, or ferromagnetic alloys, if they are composed of
    Fe, Co, and Ni.
    """
)

st.image(
    get_image_path(__file__, "comparison.png"),
    caption="Comparison of structures",
)

st.write(
    """
    The alloys of boron, silicon, phosphorus, and other glass formers with magnetic
    metals (iron, cobalt, nickel) have high magnetic susceptibility, with low coercivity
    and high electrical resistance. Usually the electrical conductivity of a metallic
    glass is of the same low order of magnitude as of a molten metal just above the
    melting point. The high resistance leads to low losses by eddy currents when
    subjected to alternating magnetic fields, a property useful for e.g. transformer
    magnetic cores. Their low coercivity also contributes to low loss.

    Amorphous metals have higher tensile yield strengths and higher elastic strain
    limits than polycrystalline metal alloys, but their ductilities and fatigue
    strengths are lower. Amorphous alloys have a variety of potentially useful
    properties. In particular, they tend to be stronger than crystalline alloys of
    similar chemical composition, and they can sustain larger reversible ("elastic")
    deformations than crystalline alloys. Amorphous metals derive their strength
    directly from their non-crystalline structure, which does not have any of the
    defects (such as dislocations) that limit the strength of crystalline alloys. One
    modern amorphous metal, known as Vitreloy, has a tensile strength that is almost
    twice that of high-grade titanium. However, metallic glasses at room temperature are
    not ductile and tend to fail suddenly when loaded in tension, which limits the
    material applicability in reliability-critical applications, as the impending
    failure is not evident. Therefore, there is considerable interest in producing metal
    matrix composites consisting of a metallic glass matrix containing dendritic
    particles or fibers of a ductile crystalline metal.

    Perhaps the most useful property of bulk amorphous alloys is that they are true
    glasses, which means that they soften and flow upon heating. This allows for easy
    processing, such as by injection molding, in much the same way as polymers. As a
    result, amorphous alloys have been commercialized for use in sports equipment,
    medical devices, and as cases for electronic equipment.
    """
)

st.header("Usage of amorphous metals")
st.subheader("Commercial")
st.write(
    """
    Currently the most important application is due to the special magnetic properties
    of some ferromagnetic metallic glasses. The low magnetization loss is used in high
    efficiency transformers (amorphous metal transformer) at line frequency and some
    higher frequency transformers. Also electronic article surveillance (such as theft
    control passive ID tags) often uses metallic glasses because of these magnetic
    properties.

    A commercial amorphous alloy, Vitreloy 1 (41.2% Zr, 13.8% Ti, 12.5% Cu, 10% Ni, and
    22.5% Be), was developed at Caltech, as a part of Department of Energy and NASA
    research of new aerospace materials.

    Ti-based metallic glass, when made into thin pipes, have a high tensile strength of
    2,100 MPa (300 ksi), elastic elongation of 2% and high corrosion resistance. Using
    these properties, a Ti-Zr-Cu-Ni-Sn metallic glass was used to improve the
    sensitivity of a Coriolis flow meter. This flow meter is about 28-53 times more
    sensitive than conventional meters, which can be applied in fossil-fuel, chemical,
    environmental, semiconductor and medical science industry.
    """
)

st.image(
    get_image_path(__file__, "coriolis.jpg"),
    caption="A mass flow meter of the Coriolis type",
)

st.write(
    """
    Zr-Al-Ni-Cu based metallic glass can be shaped into 2.2 to 5 by 4 mm (0.087 to 0.197
    by 0.157 in) pressure sensors for automobile and other industries, and these sensors
    are smaller, more sensitive, and possess greater pressure endurance compared to
    conventional stainless steel made from cold working.
    """
)

st.subheader("Potential")

st.write(
    """
    Amorphous metals exhibit unique softening behavior above their glass transition and
    this softening has been increasingly explored for thermoplastic forming of metallic
    glasses. Such low softening temperature allows for developing simple methods for
    making composites of nanoparticles (e.g. carbon nanotubes) and bulk metallic
    glasses. It has been shown that metallic glasses can be patterned on extremely small
    length scales ranging from 10 nm to several millimeters. This may solve the problems
    of nanoimprint lithography where expensive nano-molds made of silicon break easily.
    Nano-molds made from metallic glasses are easy to fabricate and more durable than
    silicon molds. The superior electronic, thermal and mechanical properties of bulk
    metallic glasses compared to polymers make them a good option for developing
    nanocomposites for electronic application such as field electron emission devices.

    Ti<sub>40</sub>Cu<sub>36</sub>Pd<sub>14</sub>Zr<sub>10</sub> is believed to be
    noncarcinogenic, is about three times stronger than titanium, and its elastic
    modulus nearly matches bones. It has a high wear resistance and does not produce
    abrasion powder. The alloy does not undergo shrinkage on solidification. A surface
    structure can be generated that is biologically attachable by surface modification
    using laser pulses, allowing better joining with bone.

    Mg<sub>60</sub>Zn<sub>35</sub>Ca<sub>5</sub>, rapidly cooled to achieve amorphous
    structure, is being investigated at Lehigh University as a biomaterial for
    implantation into bones as screws, pins, or plates, to fix fractures. Unlike
    traditional steel or titanium, this material dissolves in organisms at a rate of
    roughly 1 millimeter per month and is replaced with bone tissue. This speed can be
    adjusted by varying the content of zinc.

    Bulk metallic glasses also seem to exhibit superior properties like SAM2X5-630 which
    has the highest recorded elastic limit for any steel alloy, according to the
    researcher, essentially it has the highest threshold limit at which a material can
    withstand an impact without deforming permanently (plasticity). The alloy can
    withstand pressure and stress of up to 12.5 GPa (123,000 atm) without undergoing any
    permanent deformation, this is the highest impact resistance of any bulk metallic
    glass ever recorded (as of 2016). This makes it as an attractive option for any
    applications which requires high stress tolerance.
    """,
    unsafe_allow_html=True,
)

st.subheader("Additive manufacturing")

st.write(
    """
    One challenge when synthesizing a metallic glass is that the techniques often only
    produce very small samples, due to the need for high cooling rates. 3D-printing
    methods have been suggested as a method to create larger bulk samples. Selective
    laser melting (SLM) is one example of an additive manufacturing method that has been
    used to make iron based metallic glasses. Laser foil printing (LFP) is another
    method where foils of the amorphous metals are stacked and welded together, layer by
    layer.
    """
)
st.image(
    get_image_path(__file__, "implant.png"),
    caption="3D printed wrist joint implant",
)

st.header("What is nanoindentation?")

st.write(
    """
    In an indentation test, a hard tip whose mechanical properties are known (frequently
    made of a very hard material like diamond) is pressed into a sample whose properties
    are unknown. The load placed on the indenter tip is increased as the tip penetrates
    further into the specimen and soon reaches a user-defined value. At this point, the
    load may be held constant for a period or removed. The area of the residual
    indentation in the sample is measured and the hardness, $H$, is defined as the
    maximum load, $P_{\\mathrm{max}}$, divided by the residual indentation area,
    $A_{\\mathrm{r}}$.

    Since the mid-1970s nanoindentation has become the primary method for measuring and
    testing very small volumes of mechanical properties. Nanoindentation, also called
    depth sensing indentation or instrumented indentation, gained popularity with the
    development of machines that could record small load and displacement with high
    accuracy and precision. The load displacement data can be used to determine modulus
    of elasticity, hardness, yield strength, fracture toughness, scratch hardness and
    wear properties.

    In nanoindentation small loads and tip sizes are used, so the indentation area may
    only be a few square micrometers or even nanometers. This presents problems in
    determining the hardness, as the contact area is not easily found. Atomic force
    microscopy or scanning electron microscopy techniques may be utilized to image the
    indentation, but can be quite cumbersome. Instead, an indenter with a geometry known
    to high precision (usually a Berkovich tip, which has a three-sided pyramid
    geometry) is employed. During the course of the instrumented indentation process, a
    record of the depth of penetration is made, and then the area of the indent is
    determined using the known geometry of the indentation tip. While indenting, various
    parameters such as load and depth of penetration can be measured. A record of these
    values can be plotted on a graph to create a load-displacement curve (such as the
    one shown in the figure below). These curves can be used to extract mechanical
    properties of the material.
    """
)

st.image(
    get_image_path(__file__, "load_disp_indentation.svg"),
    caption="Indentation curve",
    use_column_width="always",
)
