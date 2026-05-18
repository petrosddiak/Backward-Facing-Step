/*---------------------------------------------------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     |
    \\  /    A nd           | www.openfoam.com
     \\/     M anipulation  |
-------------------------------------------------------------------------------
    Copyright (C) 2019-2021 OpenCFD Ltd.
    Copyright (C) YEAR AUTHOR, AFFILIATION
-------------------------------------------------------------------------------
License
    This file is part of OpenFOAM.

    OpenFOAM is free software: you can redistribute it and/or modify it
    under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    OpenFOAM is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with OpenFOAM.  If not, see <http://www.gnu.org/licenses/>.

\*---------------------------------------------------------------------------*/

#include "fixedValueFvPatchFieldTemplate.H"
#include "addToRunTimeSelectionTable.H"
#include "fvPatchFieldMapper.H"
#include "volFields.H"
#include "surfaceFields.H"
#include "unitConversion.H"
#include "PatchFunction1.H"

//{{{ begin codeInclude

//}}} end codeInclude


// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //

namespace Foam
{

// * * * * * * * * * * * * * * * Local Functions * * * * * * * * * * * * * * //

//{{{ begin localCode

//}}} end localCode


// * * * * * * * * * * * * * * * Global Functions  * * * * * * * * * * * * * //

// dynamicCode:
// SHA1 = e4d2010fdbacf9bb7337c464356e9242ffed2289
//
// unique function name that can be checked if the correct library version
// has been loaded
extern "C" void inletProfile_e4d2010fdbacf9bb7337c464356e9242ffed2289(bool load)
{
    if (load)
    {
        // Code that can be explicitly executed after loading
    }
    else
    {
        // Code that can be explicitly executed before unloading
    }
}

// * * * * * * * * * * * * * * Static Data Members * * * * * * * * * * * * * //

makeRemovablePatchTypeField
(
    fvPatchVectorField,
    inletProfileFixedValueFvPatchVectorField
);

} // End namespace Foam


// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

Foam::
inletProfileFixedValueFvPatchVectorField::
inletProfileFixedValueFvPatchVectorField
(
    const fvPatch& p,
    const DimensionedField<vector, volMesh>& iF
)
:
    parent_bctype(p, iF)
{
    if (false)
    {
        printMessage("Construct inletProfile : patch/DimensionedField");
    }
}


Foam::
inletProfileFixedValueFvPatchVectorField::
inletProfileFixedValueFvPatchVectorField
(
    const inletProfileFixedValueFvPatchVectorField& rhs,
    const fvPatch& p,
    const DimensionedField<vector, volMesh>& iF,
    const fvPatchFieldMapper& mapper
)
:
    parent_bctype(rhs, p, iF, mapper)
{
    if (false)
    {
        printMessage("Construct inletProfile : patch/DimensionedField/mapper");
    }
}


Foam::
inletProfileFixedValueFvPatchVectorField::
inletProfileFixedValueFvPatchVectorField
(
    const fvPatch& p,
    const DimensionedField<vector, volMesh>& iF,
    const dictionary& dict
)
:
    parent_bctype(p, iF, dict)
{
    if (false)
    {
        printMessage("Construct inletProfile : patch/dictionary");
    }
}


Foam::
inletProfileFixedValueFvPatchVectorField::
inletProfileFixedValueFvPatchVectorField
(
    const inletProfileFixedValueFvPatchVectorField& rhs
)
:
    parent_bctype(rhs),
    dictionaryContent(rhs)
{
    if (false)
    {
        printMessage("Copy construct inletProfile");
    }
}


Foam::
inletProfileFixedValueFvPatchVectorField::
inletProfileFixedValueFvPatchVectorField
(
    const inletProfileFixedValueFvPatchVectorField& rhs,
    const DimensionedField<vector, volMesh>& iF
)
:
    parent_bctype(rhs, iF)
{
    if (false)
    {
        printMessage("Construct inletProfile : copy/DimensionedField");
    }
}


// * * * * * * * * * * * * * * * * Destructor  * * * * * * * * * * * * * * * //

Foam::
inletProfileFixedValueFvPatchVectorField::
~inletProfileFixedValueFvPatchVectorField()
{
    if (false)
    {
        printMessage("Destroy inletProfile");
    }
}


// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //

void
Foam::
inletProfileFixedValueFvPatchVectorField::updateCoeffs()
{
    if (this->updated())
    {
        return;
    }

    if (false)
    {
        printMessage("updateCoeffs inletProfile");
    }

//{{{ begin code
    #line 31 "/home/petros/cfd_projects/step_duct/0/U/boundaryField/inlet"
const vectorField& Cf = patch().Cf();
    vectorField& field = *this;

    scalar Umax = 44.2;   // peak velocity (centerline)
    scalar n = 7.0;       // power-law exponent

    scalar y0 = 0.017;    // bottom wall
    scalar y1 = 0.050;    // top wall (CHANGE THIS)

    scalar H = y1 - y0;   // channel height

    forAll(Cf, i)
    {
        // Normalize coordinate: 0 → bottom wall, 1 → top wall
        scalar eta = (Cf[i].y() - y0) / H;

        // Clamp to avoid numerical issues
        eta = max(min(eta, 1.0), 0.0);

        // Symmetric profile (zero at both walls)
        scalar Uy = Umax * pow(4.0 * eta * (1.0 - eta), 1.0/n);

        field[i] = vector(Uy, 0, 0);
    }
//}}} end code

    this->parent_bctype::updateCoeffs();
}


// ************************************************************************* //

