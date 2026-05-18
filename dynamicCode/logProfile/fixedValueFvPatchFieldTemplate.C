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
// SHA1 = 7bac0af00fc903686ba579b06ff5d073f65245c0
//
// unique function name that can be checked if the correct library version
// has been loaded
extern "C" void logProfile_7bac0af00fc903686ba579b06ff5d073f65245c0(bool load)
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
    logProfileFixedValueFvPatchVectorField
);

} // End namespace Foam


// * * * * * * * * * * * * * * * * Constructors  * * * * * * * * * * * * * * //

Foam::
logProfileFixedValueFvPatchVectorField::
logProfileFixedValueFvPatchVectorField
(
    const fvPatch& p,
    const DimensionedField<vector, volMesh>& iF
)
:
    parent_bctype(p, iF)
{
    if (false)
    {
        printMessage("Construct logProfile : patch/DimensionedField");
    }
}


Foam::
logProfileFixedValueFvPatchVectorField::
logProfileFixedValueFvPatchVectorField
(
    const logProfileFixedValueFvPatchVectorField& rhs,
    const fvPatch& p,
    const DimensionedField<vector, volMesh>& iF,
    const fvPatchFieldMapper& mapper
)
:
    parent_bctype(rhs, p, iF, mapper)
{
    if (false)
    {
        printMessage("Construct logProfile : patch/DimensionedField/mapper");
    }
}


Foam::
logProfileFixedValueFvPatchVectorField::
logProfileFixedValueFvPatchVectorField
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
        printMessage("Construct logProfile : patch/dictionary");
    }
}


Foam::
logProfileFixedValueFvPatchVectorField::
logProfileFixedValueFvPatchVectorField
(
    const logProfileFixedValueFvPatchVectorField& rhs
)
:
    parent_bctype(rhs),
    dictionaryContent(rhs)
{
    if (false)
    {
        printMessage("Copy construct logProfile");
    }
}


Foam::
logProfileFixedValueFvPatchVectorField::
logProfileFixedValueFvPatchVectorField
(
    const logProfileFixedValueFvPatchVectorField& rhs,
    const DimensionedField<vector, volMesh>& iF
)
:
    parent_bctype(rhs, iF)
{
    if (false)
    {
        printMessage("Construct logProfile : copy/DimensionedField");
    }
}


// * * * * * * * * * * * * * * * * Destructor  * * * * * * * * * * * * * * * //

Foam::
logProfileFixedValueFvPatchVectorField::
~logProfileFixedValueFvPatchVectorField()
{
    if (false)
    {
        printMessage("Destroy logProfile");
    }
}


// * * * * * * * * * * * * * * * Member Functions  * * * * * * * * * * * * * //

void
Foam::
logProfileFixedValueFvPatchVectorField::updateCoeffs()
{
    if (this->updated())
    {
        return;
    }

    if (false)
    {
        printMessage("updateCoeffs logProfile");
    }

//{{{ begin code
    #line 32 "/home/petros/cfd_projects/step_duct/0/U/boundaryField/inlet"
const scalar kappa = 0.41;
        const scalar B = 5.2;

        const scalar nu = 1.5e-5;     // <-- CHANGE THIS to your viscosity
        const scalar uTau = 2.0;      // <-- THIS is the tuning parameter

        const vectorField& Cf = patch().Cf();
        vectorField& field = *this;

        forAll(Cf, i)
        {
            scalar y = Cf[i].y();   // distance from origin

            // --- shift to wall (IMPORTANT)
            scalar yWall = 0.0127;  // <-- your step height H
            scalar yLocal = y - yWall;

            if (yLocal < 1e-6)
            {
                field[i] = vector(0,0,0);
            }
            else
            {
                scalar uPlus = (1.0/kappa)*log(yLocal*uTau/nu) + B;
                scalar U = uPlus * uTau;

                field[i] = vector(U,0,0);
            }
        }
//}}} end code

    this->parent_bctype::updateCoeffs();
}


// ************************************************************************* //

